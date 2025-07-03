import numpy as np
import scipy.signal as sig

"""
    TO DO : améliorer get_f0 pour qu'il soit retourne toujours
    la frequence fondamentale et pas une harmonique.
"""
def _get_peak(Y, freq,lowLimit, peak):
    Y[peak] = 0
    fp = freq[peak]
    newPeak = np.argmax(Y[lowLimit:peak]) + lowLimit
    fnp = freq[newPeak]
    if fnp <= fp :
        pass
    return



def get_f0(buffer, fs, size, lowLimit=5):
    """
    buffer : float array
    fs : float (sample rate)
    size : int (buffer size)
    Estimates fundamental frequency.
    Filters out frequencies bellow lowLimit/(size*1/fs).
    """
    Y = np.abs(np.fft.rfft(buffer))

    freq = np.fft.rfftfreq(size, d=1 / fs)

    iMax = np.argmax(Y[lowLimit:]) + lowLimit
    fMax = freq[iMax]
    Y[iMax] = 0
    ##print(Y[iMax], iMax)
    iM2 = np.argmax(Y[lowLimit:]) + lowLimit
    f1 = freq[iM2]
    #print(iM2)
    if f1 <= fMax and ( fMax%f1 <= 0.1 or (fMax%f1 <= f1 +0.1 or fMax%f1 >= f1 - 0.1)):
        #print(f"Vraie f0 = {f1}")
        fMax = f1

    return fMax, f1

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
    a, b : float
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
    f0 = (get_f0(buffer1, fs, size)[0] + get_f0(buffer2, fs, size)[0]) / 2
    period = 1 / f0

    xcorr = sig.correlate(buffer1, buffer2)

    sampleShift = xcorr.argmax()
    timeShift = (sampleShift - size) / fs
    phaseShift = (timeShift / period) % 1

    return phaseShift

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    #data = np.genfromtxt(
    #    "../../../Denis Charrier/28 05 2021 - maintenance Smartprobe et acq sonification/C1 1 28 05 202100000.txt",
    #    skip_header=5,
        #delimiter=",",
   # )[1300000:1310000]
   # buffer = data.transpose()[1][0:1024]
    # plt.plot(buffer)
    # plt.show()
    fs = 100000
    size = 1024

    t = np.linspace(0, 1, fs)
    buffer = np.sin(2*np.pi*1500*t[0:1024]) + 2*np.sin(2*np.pi*3000*t[0:1024])
    B = np.abs(np.fft.rfft(buffer))
    freq = np.fft.rfftfreq(size, d = 1/fs)
    #print(get_f0(buffer, fs, size))
