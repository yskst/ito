#!/bin/env python

import sys
import fileinput
import numpy as np
import numpy.fft as fft

def getndim(data):
    ndim = 1
    sample_dim = data.size
    while ndim < sample:
        ndim *= 2
    return ndim

def main(argv):
    ndim = 0
    for l in fileinput.input():
        if l[0] == '#':
            continue
        sample = np.fromstring(l)
        if ndim == 0:
            ndim = getndim(sample)
        spectrum = fft.rfft(sample, ndim) # FFTを実行
        amp = np.abs(F)             # 振幅スペクトルを計算
        np.savetxt(sys.stdout, amp, delimiter=" ")

if __name__=='__main__':
    main(sys.argv)
