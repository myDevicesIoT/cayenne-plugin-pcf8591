"""
This module provides classes for interfacing with a PCF8591 Analog I/O extension.
"""
import time

from myDevices.devices.i2c import I2C
from myDevices.devices.analog import DAC
from myDevices.plugins.analog import AnalogInput, AnalogOutput
from myDevices.utils.logger import info

class PCF8591(DAC, I2C):
    """Base class for interacting with a PCF8591 extension."""

    def __init__(self, slave=0x48, vref=3.3):
        """Initializes PCF8591 device.

        Arguments:
        slave: The slave address
        vref: The reference voltage
        """        
        I2C.__init__(self, int(slave))
        DAC.__init__(self, 5, 8, float(vref))
        self.out_value = 0       
        
    def __str__(self):
        """Returns friendly name."""
        return "PCF8591(slave=0x%02X)" % self.slave

    def __analogRead__(self, channel, diff=False):
        """Returns the value for the specified channel. Overrides ADC.__analogRead__."""
        if (channel == 0):
            return self.out_value
        else:
            self.writeBytes(self._command(channel-1))
            return self.readBytes(3)[2]              
    
    def __analogWrite__(self, channel, value):
        """Writes the value to the specified channel. Overrides DAC.__analogWrite__."""
        if (channel == 0):
            self.out_value = value
            self.writeBytes(self._command())

    def _command(self, channel=0):
        """Format command data.

        channel: Channel on the device
        """        
        d = bytearray(2)
        d[0] = 0x40           # enable output
        d[0] |= channel & 0x03
        d[1] = self.out_value
        return d


class PCF8591Test(PCF8591):
    """Class for simulating a PCF8591 device."""

    def __init__(self):
        """Initializes the test class."""
        self.bytes = bytearray(3)
        PCF8591.__init__(self)

    def readBytes(self, size=1):
        """Read specified number of bytes."""
        return self.bytes

    def writeBytes(self, data):
        """Write data bytes."""
        self.bytes[2] = data[1]
