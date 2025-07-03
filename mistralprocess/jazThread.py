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
from acquisition.jaz import Jaz
from sync.sendData import *

class JazSonif():
    def __init__(self, jaz_ip_host : str, jaz_port : int, int_time : int, samplerate : int, pd_ip_host : str, pd_writing_port : int, pd_listening_port : int) -> None:
        """
        Wrapper for Didier Guyomarc'h's driver class for Jaz spectrometer.
        Handles Jaz data processing and communication with puredata sonification patchs.
        """
        # Connecting to Jaz
        self._spc = Jaz(ip_host=jaz_ip_host, port=jaz_port)
        self.int_time = int_time
        self._spc.set_all_integration_time(int_time)

        self.refreshrate = samplerate
        self.isOn = False

        # Setting up spectrum variables
        _3wavelengths = _spc.get_all_wave_axis()
        self.wavelengths = np.zeros(3 * NDATA)
        self.wavelengths[0:NDATA] = _3wavelengths[0]
        self.wavelengths[NDATA: NDATA * 2] = _3wavelengths[1]
        self.wavelengths[NDATA * 2: NDATA * 3] = _3wavelengths[2]

        self.il1 = 1000
        self.il2 = 1100
        self.spectrum = np.zeros(NDATA)
        self._intensiteG = 0
        self._intensiteR = 0

        # Setting up OSC Client & Server
        self._sender = udp_client.UDPClient(pd_ip_host, pd_port)

        self._dispatcher = Dispatcher()
        self._dispatcher.map("/pixel1", self._p1_handler)
        self._dispatcher.map("/pixel2", self._p2_handler)

        self._server = BlockingOSCUDPServer((pd_ip_host, pd_port), self._dispatcher)
        print("Jaz Sonification thread ready.")

    def _p1_handler(self, address, *args):
        self.il1 = int(args[0])

    def _p2_handler(self, address, *args):
        self.il2 = int(args[0])

    def _process_step(self):
        """
        Get new data from Jaz, computes new parameters and send them to puredata.
        """
        print(self.il1, self.il2)
        self.spectrum = self._spc.get_balanced_spectrum()
        self._intensiteG = get_Im(self.spectrum)
        self._intensiteR = norminf(getIrel(self.spectrum, self.il1, self.il2))
        sendMsg(self._sender, "/indexToWl", [self.wavelengths[self.il1], self.wavelengths[self.il2]])
        sendMsg(self._sender, "/iToSpc", [self.spectrum[self.il1], self.spectrum[self.il2]])
        sendMsg(self._sender, "/jazRel", self._intensiteR)
        sendMsg(self._sender, "/jazGlobal", self._intensiteG)

    def start(self):
        self.isOn = True
        self.process()

    def process(self):
        print("Jaz Sonification process started.")
        while self.isOn :
            self._process_step()
            time.sleep(1 / self.refreshrate)
        print("Jaz Sonification process stopped.")

    def pixel_input(self):
        while self.isOn :
            sendMsg(self._sender, "/poke", 1)
            self._server.handle_request()
            self._server.handle_request()


