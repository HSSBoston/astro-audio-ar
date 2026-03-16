import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def to_mono(x):
    """Convert audio to mono if it has multiple channels."""
    if x.ndim > 1:
        return x[:, 0]
    return x

def load_hrir(path, target_sr):
    """
    Load one HRIR WAV file and resample it to target_sr if needed.
    """
    hrir, sr = sf.read(path)
    hrir = to_mono(hrir)

    if sr != target_sr:
        hrir = resample_poly(hrir, target_sr, sr)

    return hrir

def binauralize_chunk(mono_chunk, hrir_left, hrir_right):
    """
    Convolve one mono chunk with left/right HRIRs and return stereo output.
    """
    left = fftconvolve(mono_chunk, hrir_left, mode="full")
    right = fftconvolve(mono_chunk, hrir_right, mode="full")
    stereo = np.column_stack((left, right))
    return stereo

# --------------------------------------------------
# 1. Load the input mono WAV
# --------------------------------------------------

input_path = "input.wav"
mono, sr_mono = sf.read(input_path)
mono = to_mono(mono)

# --------------------------------------------------
# 2. Make sure it is about 16 seconds long
# --------------------------------------------------

expected_duration_sec = 16
expected_samples = expected_duration_sec * sr_mono

if len(mono) < expected_samples:
    raise ValueError(
        f"Input audio is too short. Need at least {expected_duration_sec} seconds."
    )

# If the file is longer than 16 seconds, keep only the first 16 seconds.
mono = mono[:expected_samples]

# --------------------------------------------------
# 3. Define the 4 target elevations
# --------------------------------------------------

azimuth = 90
elevations = [0, 30, 60, 90]

# --------------------------------------------------
# 4. Map each elevation to its HRIR files
#    Change these filenames if your folder uses different names.
# --------------------------------------------------

hrir_files = {
    0: {
        "left":  "hrtf/mit-kemar/elev0/L0e090a.wav",
        "right": "hrtf/mit-kemar/elev0/R0e090a.wav",
    },
    30: {
        "left":  "hrtf/mit-kemar/elev30/L30e090a.wav",
        "right": "hrtf/mit-kemar/elev30/R30e090a.wav",
    },
    60: {
        "left":  "hrtf/mit-kemar/elev60/L60e090a.wav",
        "right": "hrtf/mit-kemar/elev60/R60e090a.wav",
    },
    90: {
        "left":  "hrtf/mit-kemar/elev90/L90e090a.wav",
        "right": "hrtf/mit-kemar/elev90/R90e090a.wav",
    },
}

# --------------------------------------------------
# 5. Split the input into four 4-second chunks
# --------------------------------------------------

chunk_duration_sec = 4
chunk_samples = chunk_duration_sec * sr_mono

chunks = [
    mono[0 * chunk_samples : 1 * chunk_samples],
    mono[1 * chunk_samples : 2 * chunk_samples],
    mono[2 * chunk_samples : 3 * chunk_samples],
    mono[3 * chunk_samples : 4 * chunk_samples],
]

# --------------------------------------------------
# 6. Binauralize each chunk with a different elevation
# --------------------------------------------------

binaural_chunks = []

for chunk, elev in zip(chunks, elevations):
    left_hrir = load_hrir(hrir_files[elev]["left"], sr_mono)
    right_hrir = load_hrir(hrir_files[elev]["right"], sr_mono)

    stereo_chunk = binauralize_chunk(chunk, left_hrir, right_hrir)
    binaural_chunks.append(stereo_chunk)

# --------------------------------------------------
# 7. Concatenate all four stereo chunks
# --------------------------------------------------

final_stereo = np.concatenate(binaural_chunks, axis=0)

# --------------------------------------------------
# 8. Normalize to avoid clipping
# --------------------------------------------------

max_val = np.max(np.abs(final_stereo))
if max_val > 0:
    final_stereo = 0.95 * final_stereo / max_val

# --------------------------------------------------
# 9. Save the final output
# --------------------------------------------------

output_path = "binaural_elevation_sequence.wav"
sf.write(output_path, final_stereo, sr_mono)

print(f"Saved: {output_path}")