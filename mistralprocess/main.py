from jazThread import JazSonif
from nidaqThread import NiDaqSonif
import threading

jaz_ip_host = 147.94.187.212
jaz_port = 7654
int_time = 100000
jaz_samplerate = 1

pd_ip_host = "localhost"
pd_writing_port = 57120
pd_listening_port = 57121

lgmr1_ni_port = "Dev1/ai0"
lgmr2_ni_port = "Dev1/ai1"
pression_port = "Dev1/ai2"

lgmr_samplerate = 100000
pression_samplerate = 1
lgmr_bsize = 1024
pression_bsize = 2

jazSonif = JazSonif(jaz_ip_host=jaz_ip_host, jaz_port=jaz_port, int_time=int_time, samplerate=jaz_samplerate,
                    pd_ip_host=pd_ip_host, pd_writing_port=pd_writing_port, pd_listening_port=pd_listening_port)

probeSonif = NiDaqSonif(lgmr1_ni_port=lgmr1_ni_port, lgmr2_ni_port=lgmr2_ni_port, pression_ni_port=pression_port, lgmr_samplerate=lgmr_samplerate, lgmr_buffersize=lgmr_bsize, pression_samplerate=pression_samplerate, pression_buffersize=pression_bsize, pd_ip_host=pd_ip_host, pd_writing_port=pd_writing_port)

jthrd = threading.Thread(target = jazSonif.start)
jpthrd = threading.Thread(target = jazSonif.pixel_input)

pthrd = threading.Thread(target=probeSonif.start)
