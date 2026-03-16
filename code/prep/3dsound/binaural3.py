import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly


# --------------------------------------------------
# 1. Settings
# --------------------------------------------------
stream_sr = 48000
blocksize = 512

mono_wav_path = "io/helicopter-hovering-01.wav"
hrir_left_path = "hrtf/mit-kemar/elev0/L0e090a.wav"
hrir_right_path = "hrtf/mit-kemar/elev0/R0e090a.wav"


# --------------------------------------------------
# 2. Helper functions
# --------------------------------------------------
def to_mono(x):
    if x.ndim > 1:
        return x[:, 0]
    return x


def load_and_resample_wav(path, target_sr):
    audio, sr = sf.read(path)
    audio = to_mono(audio)

    if sr != target_sr:
        audio = resample_poly(audio, target_sr, sr)

    return audio.astype(np.float32)


# --------------------------------------------------
# 3. Load mono WAV and HRIRs once
# --------------------------------------------------
mono_audio = load_and_resample_wav(mono_wav_path, stream_sr)
hrir_left = load_and_resample_wav(hrir_left_path, stream_sr)
hrir_right = load_and_resample_wav(hrir_right_path, stream_sr)

if len(hrir_left) < 1 or len(hrir_right) < 1:
    raise ValueError("HRIR files must not be empty.")

# Position in the looping mono WAV
playhead = 0

# Tail buffers for overlap-add
tail_left = np.zeros(len(hrir_left) - 1, dtype=np.float32)
tail_right = np.zeros(len(hrir_right) - 1, dtype=np.float32)


# --------------------------------------------------
# 4. Function to get the next looping mono block
# --------------------------------------------------
def get_next_mono_block(num_frames):
    global playhead

    output = np.empty(num_frames, dtype=np.float32)
    written = 0

    while written < num_frames:
        remaining_in_file = len(mono_audio) - playhead
        remaining_needed = num_frames - written
        n = min(remaining_in_file, remaining_needed)

        output[written:written + n] = mono_audio[playhead:playhead + n]

        written += n
        playhead += n

        # If we reached the end, wrap around to the beginning
        if playhead >= len(mono_audio):
            playhead = 0

    return output


# --------------------------------------------------
# 5. Audio callback
# --------------------------------------------------
def callback(outdata, frames, time, status):
    global tail_left, tail_right

    if status:
        print(status)

    # Get the next mono block from the looping WAV
    mono_block = get_next_mono_block(frames)

    # Full convolution for this block
    conv_left = fftconvolve(mono_block, hrir_left, mode="full").astype(np.float32)
    conv_right = fftconvolve(mono_block, hrir_right, mode="full").astype(np.float32)

    # Add the previous tail into the beginning
    conv_left[:len(tail_left)] += tail_left
    conv_right[:len(tail_right)] += tail_right

    # Output exactly 'frames' samples now
    out_left = conv_left[:frames]
    out_right = conv_right[:frames]

    # Save the new tail for the next callback
    tail_left = conv_left[frames:]
    tail_right = conv_right[frames:]

    # Simple safety normalization to reduce clipping risk
    stereo = np.column_stack((out_left, out_right))
    max_val = np.max(np.abs(stereo))
    if max_val > 1.0:
        stereo = stereo / max_val * 0.95

    outdata[:, 0] = stereo[:, 0]
    outdata[:, 1] = stereo[:, 1]


# --------------------------------------------------
# 6. Start output stream
# --------------------------------------------------
with sd.OutputStream(
    samplerate=stream_sr,
    blocksize=blocksize,
    channels=2,
    dtype="float32",
    callback=callback
):
    print("Looping binaural playback is running. Press Ctrl+C to stop.")
    while True:
        sd.sleep(1000)