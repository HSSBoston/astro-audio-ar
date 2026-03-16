import time
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly


# ==================================================
# 1. Settings
# ==================================================
stream_sr = 48000
blocksize = 512

mono_wav_path = "io/bootes.wav"

# Update interval for the fake device-direction emulator
emulator_update_sec = 0.5

# Available HRIR files
hrir_paths = [
    ("hrtf/mit-kemar/elev0/L0e090a.wav", "hrtf/mit-kemar/elev0/R0e090a.wav"),
    ("hrtf/mit-kemar/elev0/L0e060a.wav", "hrtf/mit-kemar/elev0/R0e060a.wav"),
    ("hrtf/mit-kemar/elev0/L0e030a.wav", "hrtf/mit-kemar/elev0/R0e030a.wav"),
    ("hrtf/mit-kemar/elev0/L0e000a.wav", "hrtf/mit-kemar/elev0/R0e000a.wav"),
    ("hrtf/mit-kemar/elev0/L0e330a.wav", "hrtf/mit-kemar/elev0/R0e330a.wav"),
    ("hrtf/mit-kemar/elev0/L0e300a.wav", "hrtf/mit-kemar/elev0/R0e300a.wav"),
    ("hrtf/mit-kemar/elev0/L0e270a.wav", "hrtf/mit-kemar/elev0/R0e270a.wav"),
]


# ==================================================
# 2. Helpers
# ==================================================
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


def parse_kemar_direction(path):
    """
    Example filename:
        L0e090a.wav
    returns:
        (elevation=0, azimuth=90)
    """
    filename = path.split("/")[-1]  # e.g. L0e090a.wav
    stem = filename.replace(".wav", "")
    e_index = stem.index("e")
    a_index = stem.index("a")

    elevation = int(stem[1:e_index])
    azimuth = int(stem[e_index + 1:a_index])
    return elevation, azimuth


def circular_azimuth_diff(a, b):
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)


def find_nearest_direction(target_elev, target_azim, available_dirs):
    """
    Nearest-neighbor lookup.
    Score = elevation difference + circular azimuth difference
    """
    best_dir = None
    best_score = None

    for elev, azim in available_dirs:
        score = abs(elev - target_elev) + circular_azimuth_diff(azim, target_azim)
        if best_score is None or score < best_score:
            best_score = score
            best_dir = (elev, azim)

    return best_dir


def resize_tail(old_tail, new_length):
    current_length = len(old_tail)

    if current_length == new_length:
        return old_tail

    if current_length < new_length:
        return np.pad(old_tail, (0, new_length - current_length), mode="constant")

    return old_tail[:new_length]


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


# ==================================================
# 3. Load mono WAV
# ==================================================
mono_audio = load_and_resample_wav(mono_wav_path, stream_sr)

if len(mono_audio) == 0:
    raise ValueError("Mono WAV file is empty.")


# ==================================================
# 4. Load all HRIR pairs into a direction map
# ==================================================
hrir_map = {}
available_dirs = []

for left_path, right_path in hrir_paths:
    hrir_left = load_and_resample_wav(left_path, stream_sr)
    hrir_right = load_and_resample_wav(right_path, stream_sr)

    if len(hrir_left) == 0 or len(hrir_right) == 0:
        raise ValueError(f"HRIR file is empty: {left_path} or {right_path}")

    direction = parse_kemar_direction(left_path)  # (elevation, azimuth)
    hrir_map[direction] = (hrir_left, hrir_right)
    available_dirs.append(direction)

if len(hrir_map) == 0:
    raise ValueError("No HRIR pairs loaded.")


# ==================================================
# 5. Shared direction state for emulator -> callback
# ==================================================
direction_lock = threading.Lock()

# This is the emulated device direction
target_direction = {
    "elevation": 0,
    "azimuth": 90
}


# ==================================================
# 6. Emulator thread
# ==================================================
def emulator_loop():
    """
    Fake component (2): emulate changing device direction.

    You can replace this scripted path with:
    - values read from a sensor
    - a file
    - keyboard input
    - a test trajectory
    """
    scripted_path = [
        (0, 90),
        (0, 60),
        (0, 30),
        (0, 0),
        (0, 330),
        (0, 300),
        (0, 270),
        (0, 300),
        (0, 330),
        (0, 0),
        (0, 30),
        (0, 60),
    ]

    i = 0
    while True:
        elev, azim = scripted_path[i]

        with direction_lock:
            target_direction["elevation"] = elev
            target_direction["azimuth"] = azim

        i = (i + 1) % len(scripted_path)
        time.sleep(emulator_update_sec)


# ==================================================
# 7. Playback state
# ==================================================
playhead = 0

# Start with the nearest direction to the initial target
initial_direction = find_nearest_direction(
    target_direction["elevation"],
    target_direction["azimuth"],
    available_dirs
)

active_direction = initial_direction
hrir_left, hrir_right = hrir_map[active_direction]

tail_left = np.zeros(len(hrir_left) - 1, dtype=np.float32)
tail_right = np.zeros(len(hrir_right) - 1, dtype=np.float32)

overrun_count = 0
near_limit_count = 0


# ==================================================
# 8. Looping WAV block reader
# ==================================================
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


# ==================================================
# 9. Output callback
# ==================================================
def callback(outdata, frames, time_info, status):
    global active_direction
    global hrir_left, hrir_right
    global tail_left, tail_right
    global overrun_count, near_limit_count

    callback_start = time.perf_counter()

    if status:
        print(status)

    # ----------------------------------------------
    # Read the latest emulated direction
    # ----------------------------------------------
    with direction_lock:
        target_elev = target_direction["elevation"]
        target_azim = target_direction["azimuth"]

    new_direction = find_nearest_direction(target_elev, target_azim, available_dirs)

    # ----------------------------------------------
    # Switch HRIR if needed
    # ----------------------------------------------
    if new_direction != active_direction:
        new_left, new_right = hrir_map[new_direction]

        # Preserve tails across HRIR switch
        tail_left = resize_tail(tail_left, len(new_left) - 1)
        tail_right = resize_tail(tail_right, len(new_right) - 1)

        hrir_left, hrir_right = new_left, new_right
        active_direction = new_direction

    # ----------------------------------------------
    # Process one audio block
    # ----------------------------------------------
    mono_block = get_next_mono_block(frames)

    stereo_block, tail_left, tail_right = process_block(
        mono_block, hrir_left, hrir_right, tail_left, tail_right
    )

    stereo_block = normalize_block(stereo_block)
    outdata[:, 0] = stereo_block[:, 0]
    outdata[:, 1] = stereo_block[:, 1]

    # ----------------------------------------------
    # Callback timing / overrun detection
    # ----------------------------------------------
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


# ==================================================
# 10. Start emulator thread
# ==================================================
emulator_thread = threading.Thread(target=emulator_loop, daemon=True)
emulator_thread.start()


# ==================================================
# 11. Start audio stream
# ==================================================
with sd.OutputStream(
    samplerate=stream_sr,
    blocksize=blocksize,
    channels=2,
    dtype="float32",
    callback=callback
):
    print("Real-time spatial playback is running. Press Ctrl+C to stop.")
    while True:
        sd.sleep(1000)