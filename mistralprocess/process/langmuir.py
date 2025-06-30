import numpy as np
import scipy.signal as sig

"""
    TO DO : améliorer get_f0 pour qu'il soit retourne toujours
    la frequence fondamentale et pas une harmonique.
"""


def get_f0(buffer, fs, size):
    """
    buffer : float array
    fs : float (sample rate)
    size : int (buffer size)
    Estimates fundamental frequency.
    """
    Y = np.fft.rfft(buffer)

    freq = np.fft.rfftfreq(size, d=1 / fs)

    iMax = np.argmax(Y)
    fMax = freq[iMax]

    return fMax


def remove_sig(buffer, nbHarm):
    """
    buffer : float array
    nbHarm : int
    Find fundamental frequency with get_f0 and removes nbHarm
    multiples of f0
    """
    Y = np.fft.rfft(buffer)
    iList = np.zeros(nbHarm)

    for i in range(nbHarm):
        iMax = np.argmax(np.real(Y) ** 2)
        Y[iMax] = 0
        iList[i] = iMax

    y = np.fft.irfft(Y)

    return y, iList


def get_noiseRatio(buffer, nbHarm=5, a=1, b=0):
    """
    buffer : float array
    nbHarm : int
    creates an estimation of the noise signal by removing nbHarm
    harmonics from buffer signal,
    and outputs the RMS ratio between this estimation and the
    original buffer.
    """

    y, iList = remove_sig(buffer, nbHarm)

    sigRMS = np.sqrt(np.mean(buffer**2))
    noiseRMS = np.sqrt(np.mean(y**2))

    return a * noiseRMS / sigRMS - b


def get_phaseShift(buffer1, buffer2, fs, size):
    """
    buffer1 & buffer2 : float array
    fs : int (sample rate)
    size : int (buffer size)
    outputs phase difference between two buffer containing
    the same signal but time shifted.
    """
    f0 = (get_f0(buffer1, fs, size) + get_f0(buffer2, fs, size)) / 2
    period = 1 / f0

    xcorr = sig.correlate(buffer1, buffer2)

    sampleShift = xcorr.argmax()
    timeShift = (sampleShift - size) / fs
    phaseShift = (timeShift / period) % 1

    return phaseShift
