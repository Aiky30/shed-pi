# AM2320 temperature and humidity module

Read more at https://learn.adafruit.com/adafruit-am2320-temperature-humidity-i2c-sensor_

## Hardware installation

AM2320 pinout to Raspberry Pi 4B GPIO pins

AM2320 - Type - RPI pin
Pin 1 - 3.3v - Pin 1
Pin 2 - SDA - GPIO (SDA) Pin 3
Pin 3 - gnd - Pin 6
Pin 4 - SCL - GPIO (SCL) pin 5

## Software installation

Based on instructions found
here: https://learn.adafruit.com/adafruit-am2320-temperature-humidity-i2c-sensor/python-circuitpython

```
poetry add adafruit-circuitpython-am2320
```

or for Pip

```
pip3 install adafruit-circuitpython-am2320
```

```python
import time

import adafruit_am2320
import board

# create the I2C shared bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
am = adafruit_am2320.AM2320(i2c)

while True:
    print("Temperature: ", am.temperature)
    print("Humidity: ", am.relative_humidity)
    time.sleep(2)
```
