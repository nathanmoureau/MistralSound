from sync.sendData import *
from process.pression import *
from acquisition.niAq import *
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))


fs = 1
bsize = 1
lgmr_task = configAq("Dev1/ai0", fs, bsize)

buffer = np.zeros(bsize)

oscSender = udp_client.UDPClient("localhost", 57210)

print("Ready.")

while True:
    buffer[:] = getBuffer(lgmr_task)
    pression = Vtomb(buffer[0])
    sendMsg(oscSender, "/pression", pression)
