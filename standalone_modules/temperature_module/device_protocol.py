import time

import requests
from shed_pi_module_utils.base_protocol import BaseProtocol
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.shed_pi_components.ds18b20 import TempProbe
from shed_pi_module_utils.utils import check_arch_is_arm, logger

TIME_TO_SLEEP = 60  # time in seconds


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        # Installed modules
        self.temp_probe = TempProbe(submission_service=submission_service)
        self.submission_delay = TIME_TO_SLEEP
        self.submission_service = submission_service
        self.device_id: int = None

    def stop(self):
        return False

    def submit_reading(self) -> requests.Response:
        """
        Submits a reading to an external endpoint

        :return:
        """
        probe_1_temp = self.temp_probe.read_temp()

        # FIXME: Should this be a float or a string? Broke the test
        data = {"temperature": str(probe_1_temp)}

        response = self.submission_service.submit(
            device_module_id=self.device_id, data=data
        )

        return response

    def run(self):
        while not self.stop():
            self.temp_probe.submit_reading()

            time.sleep(self.submission_delay)


def main():
    if not check_arch_is_arm():
        logger.error("only rasbian os supported")
        return

    submission_service = ReadingSubmissionService()
    device = DeviceProtocol(submission_service=submission_service)

    try:
        device.startup()
        device.run()
    finally:
        device.shutdown()


if __name__ == "__main__":
    main()
