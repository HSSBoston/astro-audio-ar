import time, numpy as np
import sounddevice as sd, soundfile as sf
from scipy.signal import fftconvolve, resample_poly

monoWavPath = "io/bootes.wav"

streamSr = 48000  # sampling rate
blockSize = 1024
switchIntervalSec = 1.0

# left-right HRIR pairs
hrirPaths = [
    ("hrtf/mit-kemar/elev0/L0e090a.wav",  "hrtf/mit-kemar/elev0/R0e090a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e080a.wav",  "hrtf/mit-kemar/elev0/R0e080a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e070a.wav",  "hrtf/mit-kemar/elev0/R0e070a.wav"),
    ("hrtf/mit-kemar/elev0/L0e060a.wav",  "hrtf/mit-kemar/elev0/R0e060a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e050a.wav",  "hrtf/mit-kemar/elev0/R0e050a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e040a.wav",  "hrtf/mit-kemar/elev0/R0e040a.wav"),
    ("hrtf/mit-kemar/elev0/L0e030a.wav",  "hrtf/mit-kemar/elev0/R0e030a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e020a.wav",  "hrtf/mit-kemar/elev0/R0e020a.wav"),
#    ("hrtf/mit-kemar/elev0/L0e010a.wav",  "hrtf/mit-kemar/elev0/R0e010a.wav"),
    ("hrtf/mit-kemar/elev0/L0e000a.wav",  "hrtf/mit-kemar/elev0/R0e000a.wav"),
    ("hrtf/mit-kemar/elev0/L0e330a.wav",  "hrtf/mit-kemar/elev0/R0e330a.wav"),
    ("hrtf/mit-kemar/elev0/L0e300a.wav",  "hrtf/mit-kemar/elev0/R0e300a.wav"),
    ("hrtf/mit-kemar/elev0/L0e270a.wav",  "hrtf/mit-kemar/elev0/R0e270a.wav"),
]


def toMono(audioData):
    if audioData.ndim > 1:
        return audioData[:, 0]
    return audioData


def loadAndResampleWav(path, targetSr):
    audioData, sampleRate = sf.read(path)
    audioData = toMono(audioData)

    if sampleRate != targetSr:
        audioData = resample_poly(audioData, targetSr, sampleRate)

    return audioData.astype(np.float32)


def normalizeBlock(stereoBlock):
    maxVal = np.max(np.abs(stereoBlock))
    if maxVal > 1.0:
        stereoBlock = stereoBlock / maxVal * 0.95
    return stereoBlock


# --------------------------------------------------
# 3. Load mono WAV
# --------------------------------------------------
monoAudio = loadAndResampleWav(monoWavPath, streamSr)

if len(monoAudio) == 0:
    raise ValueError("Mono WAV file is empty.")


# --------------------------------------------------
# 4. Load all HRIR pairs into memory
# --------------------------------------------------
hrirPairs = []

for leftPath, rightPath in hrirPaths:
    hrirLeft = loadAndResampleWav(leftPath, streamSr)
    hrirRight = loadAndResampleWav(rightPath, streamSr)

    if len(hrirLeft) == 0 or len(hrirRight) == 0:
        raise ValueError(f"HRIR file is empty: {leftPath} or {rightPath}")

    hrirPairs.append((hrirLeft, hrirRight))

if len(hrirPairs) == 0:
    raise ValueError("No HRIR pairs loaded.")


# --------------------------------------------------
# 5. Playback state
# --------------------------------------------------
playhead = 0

activePairIndex = 0
samplesUntilSwitch = int(streamSr * switchIntervalSec)

hrirLeft, hrirRight = hrirPairs[activePairIndex]

# Start with zero tails
tailLeft = np.zeros(len(hrirLeft) - 1, dtype=np.float32)
tailRight = np.zeros(len(hrirRight) - 1, dtype=np.float32)

overrunCount = 0
nearLimitCount = 0


# --------------------------------------------------
# 6. Looping WAV block reader
# --------------------------------------------------
def getNextMonoBlock(numFrames):
    global playhead

    output = np.empty(numFrames, dtype=np.float32)
    written = 0

    while written < numFrames:
        remainingInFile = len(monoAudio) - playhead
        remainingNeeded = numFrames - written
        chunkSize = min(remainingInFile, remainingNeeded)

        output[written:written + chunkSize] = monoAudio[playhead:playhead + chunkSize]

        written += chunkSize
        playhead += chunkSize

        if playhead >= len(monoAudio):
            playhead = 0

    return output


# --------------------------------------------------
# 7. Convolution for one block using one HRIR pair
# --------------------------------------------------
def processBlock(monoBlock, hrirLeft, hrirRight, tailLeft, tailRight):
    convLeft = fftconvolve(monoBlock, hrirLeft, mode="full").astype(np.float32)
    convRight = fftconvolve(monoBlock, hrirRight, mode="full").astype(np.float32)

    # Add previous spillover
    convLeft[:len(tailLeft)] += tailLeft
    convRight[:len(tailRight)] += tailRight

    outLeft = convLeft[:len(monoBlock)]
    outRight = convRight[:len(monoBlock)]

    newTailLeft = convLeft[len(monoBlock):]
    newTailRight = convRight[len(monoBlock):]

    stereoBlock = np.column_stack((outLeft, outRight))
    return stereoBlock, newTailLeft, newTailRight


# --------------------------------------------------
# 8. Resize tails if HRIR length changes
# --------------------------------------------------
def resizeTail(oldTail, newLength):
    """
    Adjust an old tail buffer to a new required length.

    If the new HRIR is longer, pad with zeros.
    If the new HRIR is shorter, keep only the beginning part.
    """
    currentLength = len(oldTail)

    if currentLength == newLength:
        return oldTail

    if currentLength < newLength:
        return np.pad(oldTail, (0, newLength - currentLength), mode="constant")

    return oldTail[:newLength]


# --------------------------------------------------
# 9. Output callback
# --------------------------------------------------
def callback(outData, frames, callbackTime, status):
    global samplesUntilSwitch
    global activePairIndex
    global hrirLeft, hrirRight
    global tailLeft, tailRight
    global overrunCount, nearLimitCount

    callbackStart = time.perf_counter()
    
    if status:
        print(status)

    outputStereo = np.zeros((frames, 2), dtype=np.float32)
    written = 0

    while written < frames:
        chunkSize = min(frames - written, samplesUntilSwitch)

        monoBlock = getNextMonoBlock(chunkSize)

        stereoBlock, tailLeft, tailRight = processBlock(
            monoBlock, hrirLeft, hrirRight, tailLeft, tailRight
        )

        outputStereo[written:written + chunkSize, :] = stereoBlock
        written += chunkSize
        samplesUntilSwitch -= chunkSize

        # Time to switch HRIR pair
        if samplesUntilSwitch == 0:
            activePairIndex = (activePairIndex + 1) % len(hrirPairs)
            newLeft, newRight = hrirPairs[activePairIndex]

            # Preserve tails instead of resetting to zero
            tailLeft = resizeTail(tailLeft, len(newLeft) - 1)
            tailRight = resizeTail(tailRight, len(newRight) - 1)

            hrirLeft, hrirRight = newLeft, newRight

            samplesUntilSwitch = int(streamSr * switchIntervalSec)

    outputStereo = normalizeBlock(outputStereo)
    outData[:, 0] = outputStereo[:, 0]
    outData[:, 1] = outputStereo[:, 1]

    # --------------------------------------------------
    # 10. Callback timing / overrun detection
    # --------------------------------------------------
    elapsed = time.perf_counter() - callbackStart
    blockTime = frames / streamSr

    if elapsed > blockTime:
        overrunCount += 1
        print(
            f"WARNING: callback overrun #{overrunCount} | "
            f"elapsed={elapsed*1000:.3f} ms, "
            f"budget={blockTime*1000:.3f} ms, "
            f"ratio={elapsed/blockTime:.2f}x"
        )
    elif elapsed > 0.9 * blockTime:
        nearLimitCount += 1
        print(
            f"NOTICE: callback near limit #{nearLimitCount} | "
            f"elapsed={elapsed*1000:.3f} ms, "
            f"budget={blockTime*1000:.3f} ms, "
            f"usage={100*elapsed/blockTime:.1f}%"
        )


# --------------------------------------------------
# 11. Start stream
# --------------------------------------------------
with sd.OutputStream(
    samplerate=streamSr,
    blocksize=blockSize,
    channels=2,
    dtype="float32",
    callback=callback
):
    print("Real-time switching HRIR playback is running. Press Ctrl+C to stop.")
    while True:
        sd.sleep(1000)