import numpy as np
import scipy.signal as sig


def get_f0(buffer, fs, size):
    Y = np.fft.rfft(buffer)

    freq = np.fft.rfftfreq(size, d=1 / fs)

    iMax = np.argmax(Y)
    fMax = freq[iMax]

    return fMax


def remove_sig(buffer, nbHarm):
    Y = np.fft.rfft(buffer)
    iList = np.zeros(nbHarm)

    for i in range(nbHarm):
        iMax = np.argmax(np.real(Y) ** 2)
        Y[iMax] = 0
        iList[i] = iMax

    y = np.fft.irfft(Y)

    return y, iList


def get_noiseRatio(buffer, nbHarm=5):
    y, iList = remove_sig(buffer, nbHarm)

    sigRMS = np.sqrt(np.mean(buffer**2))
    noiseRMS = np.sqrt(np.mean(y**2))

    return noiseRMS / sigRMS


def get_phaseShift(buffer1, buffer2, fs, size):
    f0 = (get_f0(buffer1, fs, size) + get_f0(buffer2, fs, size)) / 2
    period = 1 / f0

    xcorr = sig.correlate(buffer1, buffer2)

    sampleShift = xcorr.argmax()
    timeShift = (sampleShift - size) / fs
    phaseShift = (timeShift / period) % 1

    return phaseShift
