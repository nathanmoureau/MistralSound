from process.langmuir import *
from acquisition.datafromfile import *

data = np.genfromtxt(FILE_LANGMUIR_1, delimiter=",", skip_header=5)
dataT = data[1000000:1200000].transpose()

t = dataT[0]
y = dataT[1]
sr = 96000

faxis, ps = sig.periodogram(y, fs=sr, window=("kaiser", 38))
fundBin = np.argmax(ps)
fundIndizes = getIndizesAroundPeak(ps, fundBin)
fundFrequency = faxis[fundBin]

nHarmonics = 6
harmonicFs = getHarmonics(
    fundFrequency, sr, nHarmonics=nHarmonics, aliased=True)
print("harmonics estimated :{} ".format(harmonicFs))
