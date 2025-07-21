import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE


def configAq(deviceName, fe, bsize, sample_mode=AcquisitionType.FINITE):
    """
    Configures a given device.
    """
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan(deviceName)
    task.timing.cfg_samp_clk_timing(
        fe, sample_mode=sample_mode, samps_per_chan=bsize)
    return task


def getBuffer(task):
    return task.read(READ_ALL_AVAILABLE)
