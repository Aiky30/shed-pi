"""
Code based on: https://github.com/Gozem/am2320/blob/45a20076efb9a19e91bd50f229d1cdd53f1134d4/am2320.py#L1
License at time of code reference: MIT https://github.com/Gozem/am2320/blob/45a20076efb9a19e91bd50f229d1cdd53f1134d4/LICENSE#L1
"""

import posix
import time
from dataclasses import dataclass
from fcntl import ioctl


@dataclass
class AM2320Reading:
    temperature: float
    humidity: float

    def __str__(self):
        return f"Temperature: {self.temperature}, Humidity: {self.humidity}"


class AM2320:
    I2C_ADDR = 0x5C
    I2C_SLAVE = 0x0703

    def __init__(self, i2cbus: int = 1):
        self._fd = posix.open("/dev/i2c-%d" % i2cbus, posix.O_RDWR)

        ioctl(self._fd, self.I2C_SLAVE, self.I2C_ADDR)

    def __del__(self):
        posix.close(self._fd)

    @staticmethod
    def _calc_crc16(data):
        crc = 0xFFFF
        for x in data:
            crc = crc ^ x
            for bit in range(8):
                if (crc & 0x0001) == 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    @staticmethod
    def _combine_bytes(msb, lsb):
        return msb << 8 | lsb

    def read_sensor(self) -> AM2320Reading:
        # wake AM2320 up, goes to sleep to not warm up and affect the humidity sensor
        # This write will fail as AM2320 won't ACK this write
        try:
            posix.write(self._fd, b"\0x00")
        except:
            pass
        time.sleep(0.001)  # Wait at least 0.8ms, at most 3ms

        # write at addr 0x03, start reg = 0x00, num regs = 0x04 */
        posix.write(self._fd, b"\x03\x00\x04")
        time.sleep(0.0016)  # Wait at least 1.5ms for result

        # Read out 8 bytes of result data
        # Byte 0: Should be Modbus function code 0x03
        # Byte 1: Should be number of registers to read (0x04)
        # Byte 2: Humidity msb
        # Byte 3: Humidity lsb
        # Byte 4: Temperature msb
        # Byte 5: Temperature lsb
        # Byte 6: CRC lsb byte
        # Byte 7: CRC msb byte
        data = bytearray(posix.read(self._fd, 8))

        # Check data[0] and data[1]
        if data[0] != 0x03 or data[1] != 0x04:
            raise ValueError("First two read bytes are a mismatch")

        # CRC check
        if self._calc_crc16(data[0:6]) != self._combine_bytes(data[7], data[6]):
            raise ValueError("CRC failed")

        # Temperature resolution is 16Bit,
        # temperature highest bit (Bit15) is equal to 1 indicates a
        # negative temperature, the temperature highest bit (Bit15)
        # is equal to 0 indicates a positive temperature;
        # temperature in addition to the most significant bit (Bit14 ~ Bit0)
        # indicates the temperature sensor string value.
        # Temperature sensor value is a string of 10 times the
        # actual temperature value.
        temp = self._combine_bytes(data[4], data[5])
        if temp & 0x8000:
            temp = -(temp & 0x7FFF)
        temp /= 10.0

        humi = self._combine_bytes(data[2], data[3]) / 10.0

        return AM2320Reading(
            temperature=temp,
            humidity=humi,
        )


if __name__ == "__main__":
    am2320 = AM2320(1)
    reading = am2320.read_sensor()
    print(reading)
