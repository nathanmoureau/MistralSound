import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sp
from scipy.io.wavfile import write


FILE_LANGMUIR_1 = "/home/nath/Documents/Cours/Stage/Denis Charrier/28 05 2021 - maintenance Smartprobe et acq sonification/C1 1 28 05 202100000.txt"
FILE_LANGMUIR_2 = "/home/nath/Documents/Cours/Stage/Denis Charrier/28 05 2021 - maintenance Smartprobe et acq sonification/C2 1 28 05 202100000.txt"

FILE_JAZ = "/home/nath/Documents/Cours/Stage/Denis Charrier/data/jaz/210507/Spectre_Denis_000.dat"

FILE_PRESSION = "/home/nath/Documents/Cours/Stage/Denis Charrier/sonification 07 05 2021/C3pression CMR00000.txt"

FOLDER_JAZ = "/home/nath/Documents/Cours/Stage/Denis Charrier/data/jaz/210507/"
JAZ_PREFIX = "Spectre_Denis_"

FOLDER_JAZ_2 = "/home/nath/Documents/Cours/Stage/Denis Charrier/data/jaz/210716/"
JAZ_PREFIX_2 = "xenon_"

JAZ_SPACE = 1


def enumerate2(xs, start=0, step=1):
    for i, x in enumerate(xs):
        if i == start:
            yield (start, x)
            start += step


def fromOsc(filePath, n_lines, dwnsmpl=0):
    HEADER_LENGTH = 5  # lines
    COLUMN_LENGTH = 12  # chars
    length = int((n_lines - HEADER_LENGTH) / dwnsmpl)
    print(length)
    arr1 = np.zeros(length)
    arr2 = np.zeros(length)
    with open(filePath) as f:
        for count, x in enumerate2(f, HEADER_LENGTH, step=dwnsmpl):
            # if count%1000 == 0:
            #     print(count)
            # print(count)

            if count == HEADER_LENGTH:
                i = 0

            # print(count,i)
            # print(x[:COLUMN_LENGTH])
            # _cursor_pos = 0

            ######## COMPLEX PARSER - EXCEPTION FOR Xe-Y numbers (line 1000008~) #######
            # arr1[count-HEADER_LENGTH-1], arr2[count-HEADER_LENGTH-1] = parser(x)

            ######## O(n) PARSER #########
            arr1[i], arr2[i] = brute_parser(x)
            i += 1
            # print(x[16:-1])
            # arr2[count-HEADER_LENGTH-1] = parser(x[COLUMN_LENGTH+1:-1])

            if i >= length:
                break
    print("Done.")
    return arr1, arr2


def fromJaz(filePath, n_lines):
    N_STREAMS = 3
    COLUMN_LENGTH = 14

    lambda1 = np.zeros(n_lines)
    intensity1 = np.zeros(n_lines)

    lambda2 = np.zeros(n_lines)
    intensity2 = np.zeros(n_lines)

    lambda3 = np.zeros(n_lines)
    intensity3 = np.zeros(n_lines)

    with open(filePath) as f:
        for count, x in enumerate(f):
            if count >= n_lines:
                break

            # _cursor_pos = 0

            # lambda1[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)
            # intensity1[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)

            # lambda2[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)
            # intensity2[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)

            # lambda3[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)
            # intensity3[count], _cursor_pos = getFloat(x, _cursor_pos, COLUMN_LENGTH)

            (
                lambda1[count],
                intensity1[count],
                lambda2[count],
                intensity2[count],
                lambda3[count],
                intensity3[count],
            ) = brute_getFloat(x)

    return lambda1, intensity1, lambda2, intensity2, lambda3, intensity3


def timeJaz(folderPath, filePrefix, n_files, n_lambda, d12, d23):
    npJaz = np.zeros((n_files, n_lambda * 3 - d12 - d23))
    for i in range(n_files):
        fileName = folderPath + filePrefix + "{0:03}".format(i) + ".dat"
        # print(fileName)
        l1, i1, l2, i2, l3, i3 = fromJaz(fileName, n_lambda)
        npJaz[i][0:n_lambda] = i1
        npJaz[i][n_lambda: 2 * n_lambda - d12] = i2[d12:]
        npJaz[i][2 * n_lambda - d12:] = i3[d23:]
    print("Done loading data.")
    return npJaz


def parser(string, cursor=0, dec=0, ent=0):
    n_sig = 8
    separator = n_sig + cursor + 2 * (dec)

    charc = string[cursor]
    # print(string, separator, cursor, dec, ent, charc)
    if cursor == 0 and charc == "-":
        # print(1)
        return parser(string, cursor + 1, 0, ent)
    elif charc == ".":
        # print(2)
        if ent == 1:
            separator += 1
            return dumb_parser(string[:separator]), dumb_parser(
                string[separator + 1: -1]
            )
        return parser(string, cursor + 1, 1, ent)
    elif charc == "0":
        # print(3)
        return parser(string, cursor + 1, dec, ent)
    elif dec == 0:
        # print(4)

        return parser(string, cursor + 1, dec, 1)
        # #separator +=1
        # return float(string[ : separator]), float(string[separator + 1 : -1])

    else:
        # print(5)

        return dumb_parser(string[:separator]), dumb_parser(string[separator + 1: -1])


def dumb_parser(string):
    if string[0] == ",":
        return float(string[1:])
    elif string[-1] == ",":
        return float(string[:-1])
    return float(string)


def brute_parser(string):
    sep_i = 0
    for i, c in enumerate(string):
        if c == ",":
            sep_i = i
    return float(string[:sep_i]), float(string[sep_i + 1: -1])


def brute_getFloat(string):
    sep = [0, 0, 0, 0, 0]
    count = 0
    for i, c in enumerate(string):
        if c == "\t":
            sep[count] = i
            count += 1
    # print(sep)
    return (
        float(string[0: sep[0]]),
        float(string[sep[0] + 1: sep[1]]),
        float(string[sep[1] + 1: sep[2]]),
        float(string[sep[2] + 1: sep[3]]),
        float(string[sep[3] + 1: sep[4]]),
        float(string[sep[4] + 1: -1]),
    )


def getFloat(string, i_start, length, space=JAZ_SPACE):
    # print(string)
    # print(string[i_start:i_start+length], i_start, length)
    if string[i_start] == "-":
        f = float(string[i_start: i_start + length + 1])
        i_start += length + space + 1
        return f, i_start
    f = float(string[i_start: i_start + length])
    i_start += length + space
    return f, i_start


def writeWavFromCsv(
    filepath, fileout="out.wav", delimiter=",", skip_header=5, rate=48000
):
    csv = np.genfromtxt(filepath, delimiter=delimiter, skip_header=skip_header)
    data = csv.transpose()[1]
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    write(fileout, rate, scaled)


if __name__ == "__main__":
    # DATA_PRESSION = np.genfromtxt(FILE_PRESSION, delimiter=",", skip_header=5 , skip_footer=0)
    # DPT= DATA_PRESSION.transpose()
    # print(len(DPT[0]))
    # time = [x for i,x in enumerate2(DPT[0], 0, 1000)]
    # print(len(time))

    # ampl = [x for i,x in enumerate2(DPT[1], 0, 1000)]

    # time, ampl = DPT[0], DPT[1]
    # a1, a2 = fromOsc(FILE_PRESSION,10000005, dwnsmpl=10000)
    # sos = sp.butter(16, 15, fs=50,output = 'sos' )
    # a2Filt = sp.sosfilt(sos, a2)
    # plt.plot(a1,a2Filt)
    # plt.xlabel("Time (s)")
    # plt.ylabel("Pressure")

    ############## LANGMUIR PROBE ################

    tp1 = np.genfromtxt(FILE_LANGMUIR_1, delimiter=",", skip_header=5)
    tp2 = np.genfromtxt(FILE_LANGMUIR_2, delimiter=",", skip_header=5)
    t = tp1.transpose()[0]
    p1 = tp1.transpose()[1]
    p2 = tp2.transpose()[1]

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(t, p1)
    ax1.set_title("Sonde fenêtre")
    ax2.plot(t, p2)
    ax2.set_title("Smartprobe")
    plt.xlabel("Time (a.u.)")
    plt.ylabel("Amplitude (a.u.)")

    # ~~~~~~~~~~~~~~ Custom Functions ~~~~~~~~~~ #
    # a1, a2 = fromOsc(FILE_LANGMUIR_1,2000000)
    # sos = sp.signal.butter(32, 0.2, btype='low', output='sos')
    # a2Filt = sp.signal.sosfilt(sos, a2)
    # print("Done filtering")

    # fig, (ax1, ax2) = plt.subplots(2,1,sharex=True)
    # ax1.plot(a1, a2)
    # ax1.set_title("Non filtré")
    # ax2.plot(a1, a2Filt)
    # ax2.set_title("Filtré")
    # plt.xlabel("Time (a.u.)")
    # plt.ylabel("Amplitude (a.u.)")

    ############ TIME SPECIFIC SPECTRE  ######

    # l1, i1, l2, i2, l3, i3 = fromJaz(FILE_JAZ, 2010)

    ################ TEST RECOUPEMENT ###############

    # for count,l in enumerate(l2):
    #     if abs(l-l1[2009]) <= 0.01:
    #         print(count,l)

    # for count,l in enumerate(l3):
    #     if abs(l-l2[2009]) <= 0.1:
    #         print(count,l)
    # print("Done.")

    # plt.plot(l1, i1)
    # plt.plot(l2, i2)
    # plt.plot(l3, i3)

    ########## SPECTROGRAM JAZ ##############

    # jaz2d = timeJaz(FOLDER_JAZ, JAZ_PREFIX, 76, 2010, 44, 49)
    # jaz2dT = jaz2d.transpose()
    # plt.imshow(jaz2dT, cmap="hot", origin = "lower", interpolation = "none", extent=(0, 7000, 4018, 9744))

    # plt.xlabel("Time (a.u.)")
    # plt.ylabel("Wavelength (Angstrom)")
    # plt.colorbar()

    # plt.plot(jaz2d)

    plt.show()
