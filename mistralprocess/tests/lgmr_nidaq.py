from sync.sendData import *
from process.langmuir import *
from acquisition.niAq import *
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))


fs = 100000
bsize = 1024
lgmr_task1 = configAq("Dev1/ai0", fs, bsize)
lgmr_task2 = configAq("Dev1/ai1", fs, bsize)

buffer1 = np.zeros(bsize)
buffer2 = np.zeros(bsize)
f0 = 0
snr = 0
phShift = 0

oscSender = udp_client.UDPClient("localhost", 57210)

print("Ready.")

while True:
    buffer1[:] = getBuffer(lgmr_task1)
    buffer2[:] = getBuffer(lgmr_task2)
    f0 = get_f0(buffer1, fs, bsize) / 10000
    snr = get_noiseRatio(buffer1)
    phShift = get_phaseShift(buffer1, buffer2, fs, bsize)
    sendMsg(oscSender, "/lgmr_freq", f0)
    sendMsg(oscSender, "/lgmr_noise", snr)
    sendMsg(oscSender, "/lgmr_phase", phShift)
