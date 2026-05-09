import time, numpy as np
import sounddevice as sd               # for realtime audio output
import soundfile as sf                 # for reading WAV files
from scipy.signal import fftconvolve   # for HRIR convolution 
from scipy.signal import resample_poly

monoWavPath = "io/bootes.wav"

streamSr = 48000  # sampling rate
blockSize = 1024
switchIntervalSec = 0.5

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

# Convert the input WAV to mono, if necessary
# 
def toMono(audioData):
    # Make sure it is mono
    if audioData.ndim > 1:
        return audioData[:, 0] # take the first (left-ear) channel if needed
    return audioData

# Change a given WAV's sample rate to the expected rate
# 
def loadAndResampleWav(path, targetSr):
    audioData, sampleRate = sf.read(path)
    audioData = toMono(audioData)

    if sampleRate != targetSr:
        audioData = resample_poly(audioData, targetSr, sampleRate)

    return audioData.astype(np.float32)

# Prevents clipping. If the audio volume becomes higher than 1.0, the block is
# scaled down so its peak becomes 0.95.
#
def normalizeBlock(stereoBlock):
    maxVal = np.max(np.abs(stereoBlock))
    if maxVal > 1.0:
        stereoBlock = stereoBlock / maxVal * 0.95
    return stereoBlock

# --------------------------------------------------
# 1. Load and resample the input mono WAV
# --------------------------------------------------
monoAudio = loadAndResampleWav(monoWavPath, streamSr)
if len(monoAudio) == 0:
    raise ValueError("Mono WAV file is empty.")

# --------------------------------------------------
# 2. Load all HRIR pairs into memory
# --------------------------------------------------
hrirPairs = []

for leftPath, rightPath in hrirPaths:
    hrirLeft  = loadAndResampleWav(leftPath, streamSr)
    hrirRight = loadAndResampleWav(rightPath, streamSr)

    if len(hrirLeft) == 0 or len(hrirRight) == 0:
        raise ValueError(f"HRIR file is empty: {leftPath} or {rightPath}")

    hrirPairs.append((hrirLeft, hrirRight))

if len(hrirPairs) == 0:
    raise ValueError("No HRIR pairs loaded.")

# --------------------------------------------------
# 3. Initialize playback state
# --------------------------------------------------
playhead = 0         # indicates where the code currently is in the mono WAV
activePairIndex = 0  # indicates which HRIR pair is currently being used
samplesUntilSwitch = int(streamSr * switchIntervalSec)

hrirLeft, hrirRight = hrirPairs[activePairIndex]

# Start with zero tails
tailLeft  = np.zeros(len(hrirLeft)  - 1, dtype=np.float32)
tailRight = np.zeros(len(hrirRight) - 1, dtype=np.float32)

overrunCount = 0
nearLimitCount = 0

# --------------------------------------------------
# 4. Read the next mono block
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
# 5. Convolve one mono block with one HRIR pair
# --------------------------------------------------
def processBlock(monoBlock, hrirLeft, hrirRight, tailLeft, tailRight):
    convLeft  = fftconvolve(monoBlock, hrirLeft,  mode="full").astype(np.float32)
    convRight = fftconvolve(monoBlock, hrirRight, mode="full").astype(np.float32)

    # Add the previous block’s leftover tail
    convLeft[ :len(tailLeft)]  += tailLeft
    convRight[:len(tailRight)] += tailRight

    # Takes only the current block length for immediate playback
    outLeft  = convLeft[ :len(monoBlock)]
    outRight = convRight[:len(monoBlock)]

    # The leftover part becomes the new tail
    newTailLeft  = convLeft[ len(monoBlock):]
    newTailRight = convRight[len(monoBlock):]

    # Combines left and right into stereo
    stereoBlock = np.column_stack((outLeft, outRight))
    return stereoBlock, newTailLeft, newTailRight

# --------------------------------------------------
# 6. Resize tails if HRIR length changes
#      If the next HRIR has a different length, the saved tail may be too short
#      or too long. Adjust an old tail to a new required length.
#          If the new HRIR is longer, pad with zeros.
#          If the new HRIR is shorter, keep only the beginning part.
# --------------------------------------------------
def resizeTail(oldTail, newLength):
    currentLength = len(oldTail)

    if currentLength == newLength:
        return oldTail

    if currentLength < newLength:
        return np.pad(oldTail, (0, newLength - currentLength), mode="constant")

    return oldTail[:newLength]

# --------------------------------------------------
# 7. Real-time callback function
#      sounddevice repeatedly calls this function when it needs the next
#      stereo output block. This function gets the next mono block, convolves
#      it with HRIRs, and put the stereo output block to "outData".
#
#      Usually, this function processes the whole block at once. But if an
#      HRIR switch happens in the middle of callback processing, this function
#      splits the block into smaller chunks.
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

    # Create an empty stereo output block
    outputStereo = np.zeros((frames, 2), dtype=np.float32)
    written = 0

    # Fill the output block with stereo samples
    while written < frames:
        chunkSize = min(frames - written, samplesUntilSwitch)
        monoBlock = getNextMonoBlock(chunkSize)

        # Convolution
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

    # Callback timing: overrun detection
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
# 8. Start stream
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