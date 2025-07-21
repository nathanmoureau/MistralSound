import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.split(SCRIPT_DIR)[0]

sys.path.append(os.path.dirname(MAIN_DIR + "/"))

from sync.sendData import *
from process.langmuir import *
from acquisition.niAq import *
from process.pression import *


class NiDaqSonif():
    def __init__(self, lgmr1_ni_port : str, lgmr2_ni_port : str, pression_ni_port : int, lgmr_samplerate : int, lgmr_buffersize : int, pression_samplerate : int, pression_buffersize : int, n_a : float, n_b : float, pd_ip_host : str, pd_writing_port : int) -> None:
        """
        Intended to work with National Instrument acquisition card.
        Handles probe data acquisition and communication with puredata sonification patchs.
        """
        self.lgmr_fs = lgmr_samplerate
        self.lgmr_bsize = lgmr_buffersize
        self.prs_fs = pression_samplerate
        self.prs_bsize = pression_buffersize
        self._lgmr_task1 = configAq(lgmr1_ni_port, self.lgmr_fs, self.lgmr_bsize)
        self._lgmr_task2 = configAq(lgmr2_ni_port, self.lgmr_fs, self.lgmr_bsize)
        self._pression_task = configAq(pression_ni_port, self.prs_fs, self.prs_bsize)

        self._buffer1 = np.zeros(self.lgmr_bsize)
        self._buffer2 = np.zeros(self.lgmr_bsize)
        self.f0 = 0
        self.snr = 0
        self.phShift = 0
        self.pression = 0
        self.n_a, self.n_b = n_a, n_b

        self._oscSender = udp_client.UDPClient(pd_ip_host, pd_writing_port)

        self.isOn = False

        print("Ready.")

    def start(self):
        self.isOn = True
        self.process()

    def _process_step(self):
        # Update lgmr buffers
        self._buffer1[:] = getBuffer(self._lgmr_task1)
        self._buffer2[:] = getBuffer(self._lgmr_task2)

        # Get pressure
        _raw_pression = getBuffer(self._pression_task)[0]
        self.pression = Vtomb(_raw_pression) * 1000

        # Compute parameters
        self.f0 = get_f0(self._buffer1, self.lgmr_fs, self.lgmr_bsize)[0] / 10000
        self.snr = get_noiseRatio(self._buffer1, a = self.n_a, b=self.n_b)
        self.phShift = get_phaseShift(self._buffer1, self._buffer2, self.lgmr_fs, self.lgmr_bsize)

        # Send parameters
        sendMsg(self._oscSender, "/lgmr_freq", self.f0)
        sendMsg(self._oscSender, "/lgmr_noise", self.snr)
        sendMsg(self._oscSender, "/lgmr_phase", self.phShift)
        sendMsg(self._oscSender, "/pression", self.pression)

    def process(self):
        print("NiDaq sonification process started.")
        while self.isOn:
            self._process_step()
