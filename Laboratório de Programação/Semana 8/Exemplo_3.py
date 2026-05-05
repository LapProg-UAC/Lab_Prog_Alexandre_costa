import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

fs = 1000
t = np.arange(0, 1 + 1/fs, 1/fs)

sig = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.5 * np.sin(2 * np.pi * 100 * t)

Y = np.abs(fft(sig))

freq = fftfreq(len(sig), 1/fs)

plt.plot(freq, Y)
plt.xlim(0, 200)
plt.grid()
plt.title("FFT com SciPy")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.show()