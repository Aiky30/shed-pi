import time

import adafruit_am2320
import board
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.utils import logger

# create the I2C shared bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
am = adafruit_am2320.AM2320(i2c)

while True:
    print("Temperature: ", am.temperature)
    print("Humidity: ", am.relative_humidity)
    time.sleep(2)


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        ...

    def stop(self):
        logger.info("Stopping device protocol")

    def start(self):
        logger.info("Starting device protocol")


def main():
    # The Submission service is used to record any module data
    submission_service = ReadingSubmissionService()
    device = DeviceProtocol(submission_service=submission_service)

    try:
        device.startup()
        device.start()
    finally:
        device.shutdown()


if __name__ == "__main__":
    main()
