import time, numpy as np
import sounddevice as sd, soundfile as sf
from scipy.signal import fftconvolve, resample_poly


stream_sr = 48000
blocksize = 512
switch_interval_sec = 1.0

mono_wav_path = "io/bootes.wav"

hrir_paths = [
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


def normalize_block(stereo):
    max_val = np.max(np.abs(stereo))
    if max_val > 1.0:
        stereo = stereo / max_val * 0.95
    return stereo


# --------------------------------------------------
# 3. Load mono WAV
# --------------------------------------------------
mono_audio = load_and_resample_wav(mono_wav_path, stream_sr)

if len(mono_audio) == 0:
    raise ValueError("Mono WAV file is empty.")


# --------------------------------------------------
# 4. Load all HRIR pairs into memory
# --------------------------------------------------
hrir_pairs = []

for left_path, right_path in hrir_paths:
    hrir_left = load_and_resample_wav(left_path, stream_sr)
    hrir_right = load_and_resample_wav(right_path, stream_sr)

    if len(hrir_left) == 0 or len(hrir_right) == 0:
        raise ValueError(f"HRIR file is empty: {left_path} or {right_path}")

    hrir_pairs.append((hrir_left, hrir_right))

if len(hrir_pairs) == 0:
    raise ValueError("No HRIR pairs loaded.")


# --------------------------------------------------
# 5. Playback state
# --------------------------------------------------
playhead = 0

active_pair_index = 0
samples_until_switch = int(stream_sr * switch_interval_sec)

hrir_left, hrir_right = hrir_pairs[active_pair_index]

# Start with zero tails
tail_left = np.zeros(len(hrir_left) - 1, dtype=np.float32)
tail_right = np.zeros(len(hrir_right) - 1, dtype=np.float32)


# --------------------------------------------------
# 6. Looping WAV block reader
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

        if playhead >= len(mono_audio):
            playhead = 0

    return output


# --------------------------------------------------
# 7. Convolution for one block using one HRIR pair
# --------------------------------------------------
def process_block(mono_block, hrir_left, hrir_right, tail_left, tail_right):
    conv_left = fftconvolve(mono_block, hrir_left, mode="full").astype(np.float32)
    conv_right = fftconvolve(mono_block, hrir_right, mode="full").astype(np.float32)

    # Add previous spillover
    conv_left[:len(tail_left)] += tail_left
    conv_right[:len(tail_right)] += tail_right

    out_left = conv_left[:len(mono_block)]
    out_right = conv_right[:len(mono_block)]

    new_tail_left = conv_left[len(mono_block):]
    new_tail_right = conv_right[len(mono_block):]

    stereo = np.column_stack((out_left, out_right))
    return stereo, new_tail_left, new_tail_right


# --------------------------------------------------
# 8. Resize tails if HRIR length changes
# --------------------------------------------------
def resize_tail(old_tail, new_length):
    """
    Adjust an old tail buffer to a new required length.

    If the new HRIR is longer, pad with zeros.
    If the new HRIR is shorter, keep only the beginning part.
    """
    current_length = len(old_tail)

    if current_length == new_length:
        return old_tail

    if current_length < new_length:
        return np.pad(old_tail, (0, new_length - current_length), mode="constant")

    return old_tail[:new_length]


# --------------------------------------------------
# 9. Output callback
# --------------------------------------------------
def callback(outdata, frames, timeCallback, status):
    global samples_until_switch
    global active_pair_index
    global hrir_left, hrir_right
    global tail_left, tail_right

    callback_start = time.perf_counter()
    
    if status:
        print(status)

    output_stereo = np.zeros((frames, 2), dtype=np.float32)
    written = 0

    while written < frames:
        n = min(frames - written, samples_until_switch)

        mono_block = get_next_mono_block(n)

        stereo_block, tail_left, tail_right = process_block(
            mono_block, hrir_left, hrir_right, tail_left, tail_right
        )

        output_stereo[written:written + n, :] = stereo_block
        written += n
        samples_until_switch -= n

        # Time to switch HRIR pair
        if samples_until_switch == 0:
            active_pair_index = (active_pair_index + 1) % len(hrir_pairs)
            new_left, new_right = hrir_pairs[active_pair_index]

            # Preserve tails instead of resetting to zero
            tail_left = resize_tail(tail_left, len(new_left) - 1)
            tail_right = resize_tail(tail_right, len(new_right) - 1)

            hrir_left, hrir_right = new_left, new_right

            samples_until_switch = int(stream_sr * switch_interval_sec)

    output_stereo = normalize_block(output_stereo)
    outdata[:, 0] = output_stereo[:, 0]
    outdata[:, 1] = output_stereo[:, 1]

    # --------------------------------------------------
    # 10. Callback timing / overrun detection
    # --------------------------------------------------
    elapsed = time.perf_counter() - callback_start
    block_time = frames / stream_sr

    if elapsed > block_time:
        overrun_count += 1
        print(
            f"WARNING: callback overrun #{overrun_count} | "
            f"elapsed={elapsed*1000:.3f} ms, "
            f"budget={block_time*1000:.3f} ms, "
            f"ratio={elapsed/block_time:.2f}x"
        )
    elif elapsed > 0.9 * block_time:
        near_limit_count += 1
        print(
            f"NOTICE: callback near limit #{near_limit_count} | "
            f"elapsed={elapsed*1000:.3f} ms, "
            f"budget={block_time*1000:.3f} ms, "
            f"usage={100*elapsed/block_time:.1f}%"
        )

# --------------------------------------------------
# 11. Start stream
# --------------------------------------------------
with sd.OutputStream(
    samplerate=stream_sr,
    blocksize=blocksize,
    channels=2,
    dtype="float32",
    callback=callback
):
    print("Real-time switching HRIR playback is running. Press Ctrl+C to stop.")
    while True:
        sd.sleep(1000)