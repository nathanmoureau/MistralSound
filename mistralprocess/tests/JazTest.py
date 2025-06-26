import os
import sys
import time
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))
  
from sync.sendData import *
from acquisition.jaz import *
from process.jazGlobal import *
from process.jazRelatif import *

spc = Jaz(ip_host="147.94.187.212", port=7654)
int_time = 100000
spc.set_all_integration_time(int_time)

sender = udp_client.UDPClient("localhost", 57120)

il1 = 3000
il2 = 3100

dispatcher = Dispatcher()


def p1handler(address, *args):
    il1 = int(args[0])


def p2handler(address, *args):
    il2 = int(args[0])


dispatcher.map("/pixel1", p1handler)
dispatcher.map("/pixel2", p2handler)

server = BlockingOSCUDPServer(("localhost", 57121), dispatcher)

print("Ready.")

while True:
    data = spc.get_balanced_spectrum()
    intensiteG = normalisation(data)
    intensiteR = norminf(getIrel(data))
    sendMsg(sender, "/jazRel", intensiteR)
    sendMsg(sender, "/jazGlobal", intensiteG)
    sendMsg(sender, "/poke", 1)
    server.handle_request()
    server.handle_request()
    time.sleep(0.5)
