"""

    Précis mais trop lourd, ne pourra sans doute pas fonctionner en temps réel.


"""




import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR+"/"))

from langmuir import *
from acquisition.datafromfile import *

data = np.genfromtxt(FILE_LANGMUIR_1, delimiter=",", skip_header=5)
dataT = data[1000000:1001000].transpose()

t = dataT[0]
y = dataT[1]
sr = 96000

faxis, ps = sig.periodogram(y, fs=sr, window=("kaiser", 38))
fundBin = np.argmax(ps)
fundIndizes = getIndizesAroundPeak(ps, fundBin)
fundFrequency = faxis[fundBin]

nHarmonics = 2
harmonicFs = getHarmonics(
    fundFrequency, sr, nHarmonics=nHarmonics, aliased=True)
print("harmonics estimated :{} ".format(harmonicFs))

harmonicBorders = np.zeros([2, nHarmonics], dtype=np.int16).T
fullHarmonicBins = np.array([], dtype=np.int16)
fullHarmonicBinList = []
harmPeakFreqs = []
harmPeaks = []
for i, harmonic in enumerate(harmonicFs):
    searcharea = 0.1 * fundFrequency
    estimation = harmonic

    binNum, freq = getPeakInArea(ps, faxis, estimation, searcharea)
    harmPeakFreqs.append(freq)
    harmPeaks.append(ps[binNum])
    allBins = getIndizesAroundPeak(ps, binNum, searchWidth=10)
    fullHarmonicBins = np.append(fullHarmonicBins, allBins)
    fullHarmonicBinList.append(allBins)
    harmonicBorders[i, :] = [allBins[0], allBins[-1]]
    print(freq)


fundIndizes.sort()
pFund = bandpower(ps[fundIndizes[0]: fundIndizes[-1]])  # get power of fundamental
fundRemoved = np.delete(ps, fundIndizes)  # remove the fundamental (start constructing the noise-only signal)
fAxisFundRemoved = np.delete(faxis, fundIndizes)


noisePrepared = copy.copy(ps)
noisePrepared[fundIndizes] = 0
noisePrepared[fullHarmonicBins] = 0
noiseMean = np.median(noisePrepared[noisePrepared != 0])
noisePrepared[fundIndizes] = noiseMean
noisePrepared[fullHarmonicBins] = noiseMean

noisePower = bandpower(noisePrepared)

r = 10 * np.log10(pFund / noisePower)
