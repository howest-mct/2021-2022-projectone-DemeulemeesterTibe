import spidev
import time
from RPi import GPIO
defaultspeed = 10 ** 5


class SpiClass:
    def __init__(self, bus, slave, speed=defaultspeed) -> None:
        self.bus = bus
        self.slave = slave
        self.speed = speed
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus SPI0, slave op CE 0
        self.spi.max_speed_hz = speed

    def readChannel(self, channel):

        bytes_out = [0b00000001  # of gwn 1
                     , (8 | channel) << 4, 0]
        bytes_in = self.spi.xfer(bytes_out)
        waarde = ((bytes_in[1] & 3) << 8) | bytes_in[2]
        return waarde

    def close(self):
        self.spi.close()