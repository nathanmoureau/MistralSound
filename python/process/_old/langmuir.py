import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.signal as sig
import copy


def bandpower(ps, mode='psd'):
    """
    estimate bandpower, see https://de.mathworks.com/help/signal/ref/bandpower.html
    """
    if mode=='time':
        x = ps
        l2norm = np.linalg.norm(x)**2./len(x)
        return l2norm
    elif mode == 'psd':
        return sum(ps)        

def getIndizesAroundPeak(arr, peakIndex,searchWidth=1000):
    peakBins = []
    magMax = arr[peakIndex]
    curVal = magMax
    for i in range(searchWidth):
        newBin = peakIndex+i
        newVal = arr[newBin]
        if newVal>curVal:
            break
        else:
            peakBins.append(int(newBin))
            curVal=newVal
    curVal = magMax
    for i in range(searchWidth):
        newBin = peakIndex-i
        newVal = arr[newBin]
        if newVal>curVal:
            break
        else:
            peakBins.append(int(newBin))
            curVal=newVal
    return np.array(list(set(peakBins)))

def freqToBin(fAxis, Freq):
    return np.argmin(abs(fAxis-Freq))

def getPeakInArea(psd, faxis, estimation, searchWidthHz = 10):
    """
    returns bin and frequency of the maximum in an area
    """
    binLow = freqToBin(faxis, estimation-searchWidthHz)
    binHi = freqToBin(faxis, estimation+searchWidthHz)
    peakbin = binLow+np.argmax(psd[binLow:binHi])
    return peakbin, faxis[peakbin]

def getHarmonics(fund,sr,nHarmonics=6,aliased=False):
    harmonicMultipliers = np.arange(2,nHarmonics+2)
    harmonicFs = fund*harmonicMultipliers
    if not aliased:
        harmonicFs[harmonicFs>sr/2] = -1
        harmonicFs = np.delete(harmonicFs,harmonicFs==-1)
    else:
        nyqZone = np.floor(harmonicFs/(sr/2))
        oddEvenNyq = nyqZone%2  
        harmonicFs = np.mod(harmonicFs,sr/2)
        harmonicFs[oddEvenNyq==1] = (sr/2)-harmonicFs[oddEvenNyq==1]
    return harmonicFs   



