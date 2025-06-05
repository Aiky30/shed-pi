import time

import adafruit_am2320
import board
from shed_pi_module_utils.base_protocol import BaseProtocol
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.utils import logger


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        super().__init__(submission_service=submission_service)
        # create the I2C shared bus
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        self.component = adafruit_am2320.AM2320(i2c)

        self.should_stop = False

    def stop(self):
        logger.info("Stopping device protocol")

        self.should_stop = True

    def start(self, run_for: float = 60):
        """
        :param run_for: Time to wait between reads
        """
        logger.info("Starting device protocol")

        while not self.should_stop:
            self.read_data()
            time.sleep(run_for)

    def shutdown(self) -> None:
        self.stop()

    def run(self):
        ...

    def read_data(self):
        logger.debug("Reading component ")
        print("Temperature: ", self.component.temperature)
        print("Humidity: ", self.component.relative_humidity)

        self.submission_service.submit()


def run_protocol():
    # The Submission service is used to record any module data
    submission_service = ReadingSubmissionService()
    device = DeviceProtocol(submission_service=submission_service)

    try:
        device.start()
    finally:
        device.shutdown()


if __name__ == "__main__":
    run_protocol()
