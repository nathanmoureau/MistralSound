import os
import sys
import time
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import matplotlib.pyplot as plt

# Setting up Path
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))

from process.jazRelatif import *
from process.jazGlobal import *
from acquisition.jaz import *
from sync.sendData import *

# Connecting to Jaz
spc = Jaz(ip_host="10.16.32.4", port=7654)
int_time = 100000
spc.set_all_integration_time(int_time)

_3wavelengths = spc.get_all_wave_axis()
wavelengths = np.zeros(3 * NDATA)
wavelengths[0:NDATA] = _3wavelengths[0]
wavelengths[NDATA: NDATA * 2] = _3wavelengths[1]
wavelengths[NDATA * 2: NDATA * 3] = _3wavelengths[2]

il1 = 1000
il2 = 1100
spectrum = spc.get_balanced_spectrum()

# Setting up OSC Client & Server
sender = udp_client.UDPClient("localhost", 57120)

dispatcher = Dispatcher()


def p1handler(address, *args):
    global il1
    il1 = int(args[0])


def p2handler(address, *args):
    global il2
    il2 = int(args[0])


dispatcher.map("/pixel1", p1handler)
dispatcher.map("/pixel2", p2handler)

server = BlockingOSCUDPServer(("localhost", 57121), dispatcher)

# Setting up plot
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
(line1, ) = ax.plot(wavelengths, spectrum, "r-")

print("Ready.")

while True:
    print(il1, il2)
    spectrum = spc.get_balanced_spectrum()
    intensiteG = get_Im(spectrum)
    intensiteR = norminf(getIrel(spectrum, il1, il2))
    sendMsg(sender, "/indexToWl", [wavelengths[il1], wavelengths[il2]])
    sendMsg(sender, "/iToSpc", [spectrum[il1], spectrum[il2]])
    sendMsg(sender, "/jazRel", intensiteR)
    sendMsg(sender, "/jazGlobal", intensiteG)
    sendMsg(sender, "/poke", 1)
    server.handle_request()
    server.handle_request()
    line1.set_ydata(spectrum)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(2)
