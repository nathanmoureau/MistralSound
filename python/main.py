from JazThread import JazSonif
from ProbeThread import NiDaqSonif
import threading
import matplotlib.pyplot as plt
import time
import tomllib


# Importing Settings from configuration.toml
with open("configuration.toml", mode="rb") as f:
    config = tomllib.load(f)


jaz_ip_host = config['jaz']['jaz_ip_host']
jaz_port = config['jaz']['jaz_port']
int_time = config['jaz']['int_time']
jaz_samplerate = config['jaz']['jaz_samplerate']

pd_ip_host = config['pd']['pd_ip_host']
pd_writing_port = config['pd']['pd_writing_port']
pd_listening_port = config['pd']['pd_listening_port']

lgmr1_ni_port = config['probe']['lgmr1_ni_port']
lgmr2_ni_port = config['probe']['lgmr2_ni_port']
pression_port = config['probe']['pression_port']
lgmr_samplerate = config['probe']['lgmr_samplerate']
pression_samplerate = config['probe']['pression_samplerate']
lgmr_bsize = config['probe']['lgmr_bsize']
pression_bsize = config['probe']['pression_bsize']
noise_a = config['probe']['noise_a']
noise_b = config['probe']['noise_b']


# Initializing Daq & communications
jazSonif = JazSonif(jaz_ip_host, jaz_port, int_time, jaz_samplerate, pd_ip_host, pd_writing_port, pd_listening_port)

probeSonif = NiDaqSonif(lgmr1_ni_port, lgmr2_ni_port, pression_port, lgmr_samplerate, lgmr_bsize, pression_samplerate, pression_bsize, noise_a, noise_b, pd_ip_host, pd_writing_port)


# Thread Managing
jthrd = threading.Thread(target = jazSonif.start)
jpthrd = threading.Thread(target = jazSonif.pixel_input)
pthrd = threading.Thread(target=probeSonif.start)
gthrd = threading.Thread(target=jazSonif.graph)


jthrd.start()
jpthrd.start()
pthrd.start()
gthrd.start()

jthrd.join()
jpthrd.join()
pthrd.join()
gthrd.join()
