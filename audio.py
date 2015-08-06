import numpy as np
from scipy.io.wavfile import write

def gen_wave(f, fs, duration):
    n = duration * fs
    t = np.linspace(0, duration, n+1)
    y = np.float32([f(time) for time in t])
    return y

def rosenberg_glottal_pluse(t):
    T1 = 0.004
    T2 = 0.002
    if t >= 0 and t <= T1:
        return 0.5*(1-np.cos(np.pi*t/T1))
    elif t >= T1 and t <= T1+T2:
        return np.cos(np.pi*(t-T1)/(2*T2))
    else:
        return 0

fs = 44100
pulse = gen_wave(rosenberg_glottal_pluse, fs, 0.008)

Ug = np.fft.fft(pulse)
V = []
l = 14.5
c = 35000
N = len(Ug)
for k in range(N):
    omega = 2*np.pi*k/N
    V.append(Ug[k]/np.cos(omega*l/c))

U = np.float32(abs(np.fft.ifft(V)))


wave = np.float32([])
for i in range(0, 100):
    wave = np.append(wave, pulse)


write('test.wav', fs, wave)
