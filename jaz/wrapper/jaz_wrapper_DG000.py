# !/usr/bin/env python3
# coding: utf-8

# add environment variables PATH=
# C:\Anaconda3\envs\py37;C:\Anaconda3\envs\py37\Library\mingw-w64\bin;
# C:\Anaconda3\envs\py37\Library\usr\bin;C:\Anaconda3\envs\py37\Library\bin;C:\Anaconda3\envs\py37\Scripts;
# C:\Anaconda3\envs\py37\bin;C:\Anaconda3\condabin;
# C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME

import ctypes
import sys
import clr
import System
from System.Reflection import Assembly

# NETOmniDLL = ctypes.cdll.LoadLibrary("C:\\Program Files\\Ocean Optics\\OmniDriverSPAM\\OOI_HOME\\NETOmniDriver-NET40.dll")
# NETOmniDLL = ctypes.cdll.LoadLibrary("NETOmniDriver-NET40.dll")

# NETOmniDLL = ctypes.WinDLL(r'C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\NETOmniDriver-NET40.dll')
#.RemoteNetworksSpectrometer("147.94.187.212")


#wrapper = NETOmniDLL.wrapper.Wrapper()

# print(NETOmniDLL)
# print(getattr(NETOmniDLL, 'OmniDriver'))

# OmniDLL = ctypes.WinDLL(r'C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\OmniDriver64.dll')
# print(getattr(OmniDLL, 'Wrapper_Create'))
# wrapper = OmniDLL.Wrapper_Create(None)
# print(wrapper)
#
# commDLL = ctypes.WinDLL('C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\common64.dll')
# print(commDLL.JString_Create(None))

# NETOmni = Assembly.LoadFile(r"C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\NETOmniDriver-NET40.dll")
# wrapper = NETOmni()
# NETOmni.NETWrapper64.openNetworkSpectrometer("147.94.187.212")
# NETOmni.NETWrapperExtensions()   #.RemoteNetworkSpectrometer("147.94.187.212")

# OmniDriverDLL = ctypes.WinDLL(r'C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\OmniDriver64.dll')
# NETWrapper = OmniDriverDLL.NETWrapper64()
    # .openNetworkSpectrometer("147.94.187.212")

# OmniCommon64DLL = ctypes.WinDLL(r'C:\Program Files\Ocean Optics\OmniDriverSPAM\OOI_HOME\common64.dll')

clr.AddReference(r'NETOmniDriver_NET40.dll')

import NETOmniDriver_NET40
