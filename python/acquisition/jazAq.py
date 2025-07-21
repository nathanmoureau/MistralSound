# !/usr/bin/env python3
# coding: utf-8

"""
Didier GUYOMARC'H - 29/03/2021
See documentation "Jaz OEM Data Sheet.pdf"

TODO: read spectrum in different threads
TODO: electrical dark correction

Nathan MOUREAU - 21/07/2025
Added approximative calibration
"""

import socket
import struct
import numpy as np
# from threading import Thread

NDATA = 2048


def find_zero(r): return [i for i in range(len(r)) if r[i] == 0]


class Jaz:
    """
    Spectro
    - __init__
    - init_sock
    - close_sock
    - init_all_jaz
    - get_jaz_dpu_module_info_slots
    - get_number_spectro
    - set_current_channel
    - set_integration_time
    - set_all_integration_time
    - request_spectrum
    - get_wavelength_axis
    - get_serial_number
    - get_wave_cal
    - get_non_lin_cal
    - get_autonulling
    - get_module_info
    - request_all_spectrum

    """

    def __init__(self, **kwargs):
        # Thread.__init__(self)

        ip_host = kwargs["ip_host"]
        port = kwargs["port"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        self.sock.connect((ip_host, port))
        print("socket connected")
        # self.init_sock()

        self.fmt_request_spectrum = "<" + NDATA * "H"

        self._number_jaz = self._get_number_jaz()
        self.dpu_info = self._get_dpu_info()
        self.mod_info = self._get_modules_info()
        # print(self.mod_info)
        # print(self.dpu_info)
        # print(self._number_jaz)

        self.dark_level, self.sat_level, self.data_scale = self.get_all_auto_nulling()
        self.wave_axis = self.get_all_wave_axis()

        # self.scale = self.get_autonulling()
        # self.wave_cal_pol = self.get_wave_cal()

    @property
    def number_jaz(self):
        return self._number_jaz

    # @number_jaz.setter
    # def number_jaz(self, value):
    #     self._number_jaz = value

    # def init_sock(self):
    #     # Create a socket (TCP socket)
    #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # try:
    #     self.sock.connect((self.ip_host, self.port))
    #     print('socket connected')
    #     # finally:
    #     #     self.sock.close()
    #     #     print('socket closed')

    def close_sock(self):
        self.sock.close()

    def _get_number_jaz(self):
        """
        Get number of spectrometers.
        Command byte value : 0xC0
        Return data : 1 byte
        """
        s = b"\xc0"
        self.sock.send(s)
        r = self.sock.recv(1)
        # print(f'{r[0]} spectrometers')
        # return struct.unpack('<B', r)[0]
        return r[0]

    def _set_current_channel(self, channel):
        """
        Set current channel.
        Command byte value : 0xC1
        Command data : 1 byte for module index
        """
        s = b"\xc1" + struct.pack("<B", channel)
        self.sock.send(s)

    def _get_dpu_info(self):
        """
        Initialization of the Display and Processing Unit.
        :return:
        jaz_dpu_sn : Jaz main board serial number
        jaz_dpu_mac : MAC adress
        jaz_dpu_address : IPv4 address
        jaz_dpu_netmask : IPv4 netmask
        jaz_dpu_gateway : IPv4 gateway
        jaz_dpu_nameserver : IPv4 nameserver
        jaz_dpu_time : Time and date
        number_jaz : get number of jaz spectrometers
        """

        # Jaz DPU Module Info Slots
        index_dpu_info = [
            0x01,
            0x10,
            0x11,
            0x12,
            0x13,
            0x14,
            0x20,
            0x21,
            0x24,
            0x60,
            0x61,
            0x62,
            0x64,
            0x65,
            0x66,
            0x68,
            0x69,
            0x6A,
            0xA3,
            0xB0,
            0xC0,
        ]
        dpu_info = []
        for index in index_dpu_info:  # 0x11
            s = b"\xc6" + struct.pack("<B", index)
            self.sock.send(s)
            r = self.sock.recv(17)[2:]
            dpu_info.append(r)

        for index in range(1, 16):
            s = b"\xc6" + struct.pack("<B", 192 + index)
            self.sock.send(s)
            r = self.sock.recv(17)[2:]
            dpu_info.append(r)

        return dpu_info

    def _set_integration_time(self, channel, integration_time):
        """
        Set integration time
        Command byte value : 0x02
        Command data : 4 bytes for time in usec (LSB first up to MSB)
        """
        self._set_current_channel(channel)
        s = b"\x02" + struct.pack("<I", int(integration_time))
        self.sock.send(s)

    def set_all_integration_time(self, integration_time):
        """
        Set integration time for all channels.
        """
        for ch in range(self.number_jaz):
            self._set_integration_time(ch, integration_time)

    def _request_spectrum(self, channel):
        """
        Request spectrum for the current channel.
        Command byte value : 0x09
        Return data : 1 byte
        Notes : Initiate a spectrum acquisition. Jaz will acquire a complete spectrum (2048 pixels values)
        """
        self._set_current_channel(channel)
        s = b"\x09"  # get spectrum 1
        self.sock.send(s)
        r = self.sock.recv(2 * NDATA)  # short int = 2 bytes
        data = (
            np.array(struct.unpack(self.fmt_request_spectrum, r))
            * self.data_scale[channel]
        )
        return data

    def request_all_spectrum(self):
        """

        :return:
        """
        data = []
        for ch in range(self.number_jaz):
            data.append(self._request_spectrum(ch))
        return data

    def _get_module_info(self, channel):
        """


        :return:
        """
        mod_info = []
        self._set_current_channel(channel)
        for i in range(17):  # 0x11
            s = b"\x05" + struct.pack("<B", i)
            self.sock.send(s)
            r = self.sock.recv(17)[2:]
            mod_info.append(r)
        return mod_info

    def _get_modules_info(self):
        mod_info = []
        for ch in range(self.number_jaz):
            mod_info.append(self._get_module_info(ch))
        return mod_info

    def _wave_cal_pol(self, channel):
        """
        Get four wavelength calibration coefficients.
        :return: a list of four coefficients.
        """
        wave_cal_pol = []
        for i in range(1, 5):
            r = self.mod_info[channel][i]
            # print(f"{r=}")
            wave_cal_pol.append(float(r[: find_zero(r)[0]]))
        # print(wave_cal_pol)
        return wave_cal_pol

    def get_all_wave_cal_pol(self):
        """

        :return:
        """
        wave_cal_pol = []
        for ch in range(self.number_jaz):
            wave_cal_pol.append(self._wave_cal_pol(ch))
        return wave_cal_pol

    def _get_wave_axis(self, channel):
        """

        :param channel:
        :return:
        """

        def cal_pol(x):
            y = 0
            for i, c in enumerate(self._wave_cal_pol(channel)):
                y += c * x**i
            return y

        return [cal_pol(x) for x in range(NDATA)]

    def get_all_wave_axis(self):
        """

        :return:
        """
        self.get_all_wave_cal_pol()
        wave_axis = []
        for ch in range(self.number_jaz):
            wave_axis.append(self._get_wave_axis(ch))
        return wave_axis

    def get_non_lin_cal(self):
        """
        Get four or seven non-linearity correction coefficients.
        :return: a list of four or seven coefficients.
        """
        pass

    def _get_auto_nulling(self, channel):
        """
        Get baseline and saturation values for au-nulling.
        Index : 0x11
        """
        self._set_current_channel(channel)
        self.sock.send(b"\x05\x11")
        r = self.sock.recv(17)
        dark_level = int.from_bytes(r[4:6], byteorder="little")
        sat_level = int.from_bytes(r[6:8], byteorder="little")
        data_scale = 65535.0 / float(sat_level)
        # print(f'ch{channel}, dark level = {dark_level}')
        # print(f'ch{channel}, sat level = {sat_level}')
        return dark_level, sat_level, data_scale

    def get_all_auto_nulling(self):
        dark_level, sat_level, data_scale = [], [], []
        for ch in range(self.number_jaz):
            dl, sl, ds = self._get_auto_nulling(ch)
            dark_level.append(dl)
            sat_level.append(sl)
            data_scale.append(ds)
        return dark_level, sat_level, data_scale

    def black_body_coef(self):
        pass

    # Fonctions ajoutées par Nathan Moureau

    def _get_mean_spectrum(self, spectrum):
        return spectrum.mean()

    def get_balanced_spectrum(self):
        """
        Calibration approximative des trois sondes,
        afin de supprimer les sauts dans le spectre.
        """
        unbalanced = self.request_all_spectrum()
        mean_level = [self._get_mean_spectrum(unbalanced[i]) for i in range(3)]
        balanced = np.zeros(NDATA * 3)
        balanced[0:NDATA] = unbalanced[0] - mean_level[0]
        balanced[NDATA: NDATA * 2] = unbalanced[1] - mean_level[1]
        balanced[NDATA * 2: NDATA * 3] = unbalanced[2] - mean_level[2]
        return balanced


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # from pyqtgraph.Qt import QtGui, QtCore
    # import pyqtgraph as pg

    # Init the jaz main board ip_host, port
    spc = Jaz(ip_host="147.94.187.212", port=7654)
    jaz_mod = []
    # Init all modules
    int_time = 100000  # in usec
    spc.set_all_integration_time(int_time)
    # print(spc.get_all_auto_nulling())
    dataSp = spc.request_all_spectrum()

    balanced = spc.get_balanced_spectrum()
    plt.plot(balanced)
    plt.show()

    # app = QtGui.QApplication([])
    # win = pg.GraphicsLayoutWidget(show=True, title='')
    # pg.setConfigOptions(antialias=True)
    # p1 = win.addPlot()

    col = ["b", "g", "r"]
    crv = []
    # for i in range(3):
    #     crv.append(p1.plot(pen=col[i]))

    def update_plot():
        y = spc.request_all_spectrum()
        for i, v in enumerate(y):
            crv[i].setData(spc.wave_axis[i], v)
            # plt.plot(x[i], v)

    # plt.grid()
    # plt.show()

    # timer = QtCore.QTimer()
    # timer.timeout.connect(update_plot)
    # timer.start(100)

    # QtGui.QGuiApplication.instance().exec_()

