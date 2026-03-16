import numpy as np
import sounddevice as sd

samplerate = 48000
duration = 2

t = np.linspace(0, duration, samplerate*duration, endpoint=False)
tone = 0.3*np.sin(2*np.pi*440*t)

sd.play(tone, samplerate)
sd.wait()