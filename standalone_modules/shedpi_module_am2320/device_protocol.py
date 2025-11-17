import time
from dataclasses import dataclass
from typing import Optional

from shed_pi_module_utils.base_protocol import BaseProtocol
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.utils import logger

# TODO: uv install for the


@dataclass
class DataReading:
    temperature: float
    humidity: float

    def serialize(self) -> dict:
        return {"temperature": self.temperature, "humidity": self.humidity}


class DeviceProtocol(BaseProtocol):
    def __init__(
        self,
        submission_service: ReadingSubmissionService,
        device_module_id: int,
    ):
        super().__init__(submission_service=submission_service)

        # TODO: Get the module id, needs a mechanism to fetch, maybe a device registry by hash to lookup!
        #       Also, record errors / missing heartbeat to module
        self.device_module_id = device_module_id

        self.component: Optional[object] = None

        self._import_libraries()

        self.should_stop = False

    def _import_libraries(self):
        # FIXME: Need the libraries installing!!
        import board
        from adafruit_am2320 import AM2320

        # create the I2C shared bus
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        self.component = AM2320(i2c)

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

        reading: DataReading = DataReading(
            temperature=self.component.temperature,
            humidity=self.component.relative_humidity,
        )

        # TODO: Validate?

        self.submission_service.submit(
            device_module_id=self.device_module_id, data=reading.serialize()
        )


def run_protocol():
    # FIXME: Add a device id
    # The Submission service is used to record any module data
    submission_service = ReadingSubmissionService()
    device = DeviceProtocol(submission_service=submission_service, device_module_id=1)

    try:
        device.start()
    finally:
        device.shutdown()


if __name__ == "__main__":
    run_protocol()
