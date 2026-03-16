import os
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly


def toMono(audio):
    if audio.ndim > 1:
        return audio[:, 0]
    return audio


def loadHrir(path, targetSr):
    hrir, sr = sf.read(path)
    hrir = toMono(hrir)
    if sr != targetSr:
        hrir = resample_poly(hrir, targetSr, sr)
    return hrir


def buildKemarPath(basePath, ear, elevation, azimuth):
    folder = os.path.join(basePath, f"elev{elevation}")
    filename = f"{ear}{elevation}e{azimuth:03d}a.wav"
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return path


def normalizeAudio(stereo):
    maxVal = np.max(np.abs(stereo))
    if maxVal > 0:
        stereo = 0.95 * stereo / maxVal
    return stereo


# "trim" -> remove leftover samples at the end
# "pad"  -> add zeros at the end
#
def adjustSegmentLength(mono, numSegments, mode="trim"):
    if mode not in ["trim", "pad"]:
        raise ValueError("Mode must be either 'trim' or 'pad'")

    totalSamples = len(mono)
    remainder = totalSamples % numSegments

    if remainder == 0:
        return mono

    if mode == "trim":
        newLength = totalSamples - remainder
        print(
            f"Trimming {remainder} sample(s) from the end "
            f"so the audio splits evenly into {numSegments} segments."
        )
        return mono[:newLength]

    if mode == "pad":
        padAmount = numSegments - remainder
        print(
            f"Padding {padAmount} zero sample(s) at the end "
            f"so the audio splits evenly into {numSegments} segments."
        )
        return np.pad(mono, (0, padAmount), mode="constant")


def synthesizeBinauralSequence(inputWav, outputWav,
                               hrirBasePath, directionList,
                               saveIndividualClips=False):
    mono, srMono = sf.read(inputWav)
    mono = toMono(mono)

    numSegments = len(directionList)
    mono = adjustSegmentLength(mono, numSegments, mode="trim")

    totalSamples = len(mono)
    chunkSamples = totalSamples // numSegments

    binauralChunks = []

    for i, (elevation, azimuth) in enumerate(directionList):
        start = i * chunkSamples
        end = (i + 1) * chunkSamples
        monoChunk = mono[start:end]

        leftPath  = buildKemarPath(hrirBasePath, "L", elevation, azimuth)
        rightPath = buildKemarPath(hrirBasePath, "R", elevation, azimuth)

        hrirLeft  = loadHrir(leftPath,  srMono)
        hrirRight = loadHrir(rightPath, srMono)

        left  = fftconvolve(monoChunk, hrirLeft,  mode="full")[:len(monoChunk)]
        right = fftconvolve(monoChunk, hrirRight, mode="full")[:len(monoChunk)]
        stereoChunk = np.column_stack((left, right))

        binauralChunks.append(stereoChunk)

        if saveIndividualClips:
            clipName = f"clip_{i+1}_e{elevation}_a{azimuth}.wav"
            sf.write(clipName, normalizeAudio(stereoChunk), srMono)
            print(f"Saved individual clip: {clipName}")

    finalStereo = np.concatenate(binauralChunks, axis=0)
    finalStereo = normalizeAudio(finalStereo)
    sf.write(outputWav, finalStereo, srMono)
    print(f"Saved final output: {outputWav}")


if __name__ == "__main__":
    inputWav = "io/helicopter-hovering-01.wav"
    outputWav = "io/helicopter-hovering-01-move2.wav"
    hrirBasePath = "hrtf/mit-kemar"

    directionList = [
        (0, 90),
        (0, 45),
        (0, 0),
        (0, 315),
        (0, 275)
    ]

    synthesizeBinauralSequence(
        inputWav = inputWav,
        outputWav = outputWav,
        hrirBasePath = hrirBasePath,
        directionList = directionList,
        saveIndividualClips = False
    )
