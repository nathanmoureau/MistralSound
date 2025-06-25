from sync.sendData import *
from acquisition.jaz import *
from process.jazGlobal import *
from process.jazRelatif import *
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))

spc = Jaz(ip_host="147.94.187.212", port=7654)
int_time = 100000
spc.set_all_integration_time(int_time)

sender = udp_client.UDPClient("localhost", 57120)

il1 = 3000
il2 = 3100

print("Ready.")

while True:
    data = spc.get_balanced_spectrum()
    intensiteG = normalisation(data)
    intensiteR = norminf(getIrel(data))
    sendMsg(sender, "/jazRel", intensiteR)
    sendMsg(sender, "/jazGlobal", intensiteG)
    time.sleep(0.5)
