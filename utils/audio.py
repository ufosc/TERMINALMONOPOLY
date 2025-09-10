import numpy as np
import simpleaudio as sa
import time
# https://simpleaudio.readthedocs.io/en/latest/tutorial.html 
# calculate note frequencies
A_freq = 440
Csh_freq = A_freq * 2 ** (4 / 12)
E_freq = A_freq * 2 ** (7 / 12)

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
T = 0.25
t = np.linspace(0, T, int(T * sample_rate), False)

# generate sine wave notes
A_note = np.sin(A_freq * t * 2 * np.pi)
Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
E_note = np.sin(E_freq * t * 2 * np.pi)



notes = np.array([np.sin(100*t * i * np.pi) for i in range(11)])

# Generate a random sequence of notes
np.random.seed(int(time.time()))
random_notes = np.random.Generator(np.random.PCG64()).choice(notes, size=10)

# Concatenate the random sequence of notes
audio = np.hstack(random_notes)

# audio = np.hstack((A_note, Csh_note, E_note))

# concatenate notes
# audio = np.hstack(notes)


# normalize to 16-bit range
audio *= 32767 / np.max(np.abs(audio))
# convert to 16-bit data
audio = audio.astype(np.int16)

# start playback
play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()

print("Audio played successfully.")