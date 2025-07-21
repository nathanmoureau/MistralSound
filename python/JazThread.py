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
from acquisition.jazAq import Jaz, NDATA
from sync.sendData import *

class JazSonif():
    def __init__(self, jaz_ip_host : str, jaz_port : int, int_time : int, samplerate : int, pd_ip_host : str, pd_writing_port : int, pd_listening_port : int) -> None:
        """
        Wrapper for Didier Guyomarc'h's driver class for Jaz spectrometer.
        Handles Jaz data processing and communication with puredata sonification patchs.
        """
        # Connect to Jaz
        self._spc = Jaz(ip_host=jaz_ip_host, port=jaz_port)
        self.int_time = int_time
        self._spc.set_all_integration_time(int_time)

        self.refreshrate = samplerate
        self.isOn = False

        # Set up spectrum variables
        _3wavelengths = self._spc.get_all_wave_axis()
        self.wavelengths = np.zeros(3 * NDATA)
        self.wavelengths[0:NDATA] = _3wavelengths[0]
        self.wavelengths[NDATA: NDATA * 2] = _3wavelengths[1]
        self.wavelengths[NDATA * 2: NDATA * 3] = _3wavelengths[2]
        self.indeces = np.linspace(0, NDATA*3-1, NDATA*3)
        self.peak_index_1 = 0
        self.peak_index_2 = 0
        self.peak_threshold = 0

        self.il1 = 1000
        self.il2 = 1100
        self.spectrum = self._spc.get_balanced_spectrum() #np.zeros(NDATA*3)
        self._intensiteG = 0
        self._intensiteR = 0

        # Set up OSC Client & Server
        self._sender = udp_client.UDPClient(pd_ip_host, pd_writing_port)

        self._dispatcher = Dispatcher()
        self._dispatcher.map("/pixel1", self._p1_handler)
        self._dispatcher.map("/pixel2", self._p2_handler)
        self._dispatcher.map("/nexti1", self._next_i1)
        self._dispatcher.map("/nexti2", self._next_i2)
        self._dispatcher.map("/intTime", self._int_time_setter)
        self._dispatcher.map("/peakThrshld", self._set_threshold)

        self._server = BlockingOSCUDPServer((pd_ip_host, pd_listening_port), self._dispatcher)

        print("Jaz Sonification thread ready.")

    def _p1_handler(self, *args):
        # print(args)
        self.il1 = int(args[1])

    def _p2_handler(self, *args):
        self.il2 = int(args[1])

    def _int_time_setter(self, *args):
        """
        Sets spectrometer integration time.
        """
        # print(args)
        new_int_time = int(args[1])
        if new_int_time != self.int_time:
            self.int_time = new_int_time
            self._spc.set_all_integration_time(self.int_time)


    def _set_threshold(self, *args):
        self.peak_threshold = float(args[1])

    def _get_all_peaks(self):
        peaks = self.spectrum >= self.peak_threshold
        n_peaks = peaks.sum()
        return self.indeces[peaks], n_peaks

    def _get_next_peak(self, peak_index, n_peaks):
        if peak_index >= n_peaks:
            return 0
        else :
            return  peak_index + 1

    def _get_previous_peak(self, peak_index, n_peaks):
        if peak_index == 0:
            return n_peaks-1
        else :
            return peak_index - 1

    def _next_i1(self, *args):
        peaks_indeces, n_peaks = self._get_all_peaks()
        # print(peaks_indeces, n_peaks, self.peak_index_1)
        if args[1] == 1:
            print(1)
            # print(peaks_indeces)
            self.peak_index_1 = self._get_next_peak(self.peak_index_1, n_peaks)
        elif args[1] == 0:
            print(0)
            self.peak_index_1 = self._get_previous_peak(self.peak_index_1, n_peaks)

        self.il1 = int(peaks_indeces[self.peak_index_1])
        print(self.il1)
        sendMsg(self._sender, "/newPixel1", self.il1)

    def _next_i2(self, *args):
        peaks_indeces, n_peaks = self._get_all_peaks()
        if args[1] == 1:
            self.peak_index_2 = self._get_next_peak(self.peak_index_2, n_peaks)
        elif args[1] == 0:
            self.peak_index_2 = self._get_previous_peak(self.peak_index_2, n_peaks)
        self.il2 = int(peaks_indeces[self.peak_index_2])
        sendMsg(self._sender, "/newPixel2", self.il2)


    def _process_step(self):
        """
        Gets new data from Jaz, computes new parameters and send them to puredata.
        """
        print(self.il1, self.il2)
        self.spectrum = self._spc.get_balanced_spectrum()
        self._intensiteG = get_Im(self.spectrum)
        self._intensiteR = norminf(getIrel(self.spectrum, self.il1, self.il2))
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
        """
        Sends a "/poke" message and waits for 4 messages : /pixel1, /pixel2, /intTime & /peakThrshld
        """
        while self.isOn :
            sendMsg(self._sender, "/poke", 1)
            self._server.handle_request()
            self._server.handle_request()
            self._server.handle_request()
            self._server.handle_request()
            sendMsg(self._sender, "/indexToWl", [self.wavelengths[self.il1], self.wavelengths[self.il2]])
            time.sleep(0.1)

    def graph(self):
        """
        Plots spectrometer data.
        """
        plt.ion()
        px1 = np.ones(NDATA*3)
        px2 = np.ones(NDATA*3)
        y = np.linspace(0, 5000, NDATA*3)
        xthrshld = np.linspace(350, 950, NDATA*3)
        ythrshld = np.ones(NDATA*3)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim([350, 1000])
        (line1, ) = ax.plot(self.wavelengths, self.spectrum, "r-")
        (lpx1, ) = ax.plot(self.il1 * px1, y, 'b+')
        (lpx2, ) = ax.plot(self.il2 * px2, y, 'g+')
        (thrshld, ) = ax.plot(xthrshld, ythrshld * self.peak_threshold, 'y*')
        while self.isOn:
            lpx1.set_xdata(self.wavelengths[self.il1] * px1)
            lpx2.set_xdata(self.wavelengths[self.il2] * px2)
            line1.set_ydata(self.spectrum)
            thrshld.set_ydata(self.peak_threshold * ythrshld)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(1/ self.refreshrate)

