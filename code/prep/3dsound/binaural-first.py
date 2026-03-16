import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve
from scipy.signal import resample_poly

inputWav  = "io/helicopter-hovering-01"

inputWavFileName  = inputWav + ".wav"
outputWavFileName = inputWav + "-binaural.wav"

hrtfLeft  = "hrtf/mit-kemar/elev0/L0e090a.wav"
hrtfRight = "hrtf/mit-kemar/elev0/R0e090a.wav"

# Load the input Wav file
mono, sr_mono = sf.read(inputWavFileName)

# Make sure it is mono
if mono.ndim > 1:
    mono = mono[:, 0]  # take the first channel if needed

# Load HRTFs
hrtf_left, sr_left = sf.read(hrtfLeft)
hrtf_right, sr_right = sf.read(hrtfRight)

# Make sure HRTFs are mono too
if hrtf_left.ndim > 1:
    hrtf_left = hrtf_left[:, 0]
if hrtf_right.ndim > 1:
    hrtf_right = hrtf_right[:, 0]

# Check sampling rates
if not (sr_mono == sr_left == sr_right):
    print("Input sampling rate:", sr_mono)
    print("HRTF L sampling rate:", sr_left)
    print("HRTF R sampling rate:", sr_right)
    if sr_left != sr_mono:
        hrtf_left = resample_poly(hrtf_left, sr_mono, sr_left)
    if sr_right != sr_mono:
        hrtf_right = resample_poly(hrtf_right, sr_mono, sr_right)
    print("Resampled HRTF sampling rates")
    

# --------------------------------------------------
# 4. Convolve mono sound with each HRTF
# --------------------------------------------------
left_out = fftconvolve(mono, hrtf_left, mode="full")
right_out = fftconvolve(mono, hrtf_right, mode="full")

# --------------------------------------------------
# 5. Stack into stereo
# --------------------------------------------------
stereo = np.column_stack((left_out, right_out))

# --------------------------------------------------
# 6. Normalize so the sound does not clip
# --------------------------------------------------
max_val = np.max(np.abs(stereo))
if max_val > 0:
    stereo = stereo / max_val * 0.95

# --------------------------------------------------
# 7. Save output
# --------------------------------------------------
sf.write(outputWavFileName, stereo, sr_mono)

print("Saved as", outputWavFileName)