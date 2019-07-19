#!/usr/bin/env python
# vim:fileencoding=utf-8

import numpy as np
#import matplotlib.pyplot as plt

import numpy.fft as fft
import scipy.io.wavfile as siw


fs = 48000
gain = 100.0
def tsp():
    #plt.close("all")

    # parameters
    global fs,gain
    N_exp = 16
    m_exp = 2
    nrepeat = 5

    N = 2 ** N_exp
    m = N // (2 ** m_exp)  # (J=2m)
    a = ((m * np.pi) * (2.0 / N) ** 2)

    tsp_freqs = np.zeros(N, dtype=np.complex128)
    tsp_freqs[:(N // 2) + 1] = np.exp(-1j * a * (np.arange((N // 2) + 1) ** 2))
    tsp_freqs[(N // 2) + 1:] = np.conj(tsp_freqs[1:(N // 2)][::-1])

    # ifft and real
    tsp = np.real(fft.ifft(tsp_freqs, N))

    # roll
    tsp = gain * np.roll(tsp, (N // 2) - m)

    # repeat
    tsp_repeat = np.array(np.r_[np.tile(tsp, nrepeat), np.zeros(N)])

    print(type(tsp_repeat.dtype))

    # write
    siw.write("tsp.wav", fs, tsp_repeat)

    #fig = plt.figure(1)
    #ax = fig.add_subplot(211)
    #ax.plot(tsp)
    #ax = fig.add_subplot(212)
    #ax.plot(tsp_repeat)

    #plt.show()
def white_noise():
   global fs,gain
   stop = 100
   y1 = np.random.rand(fs * stop) - 0.5
   y11 = np.real(np.fft.fft(y1)/float(fs * stop /2)) * gain
   siw.write("white.wav", fs, y11)

if __name__=='__main__':
    white_noise()
   
