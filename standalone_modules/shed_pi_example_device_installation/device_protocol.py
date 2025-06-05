import time
from typing import Optional

import requests
from shed_pi_module_utils.base_protocol import BaseProtocol
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.shed_pi_components.ds18b20 import TempProbe
from shed_pi_module_utils.utils import check_arch_is_arm, logger

from standalone_modules.rpi.device import RPIDevice

TIME_TO_SLEEP = 60  # time in seconds


class DeviceProtocol(BaseProtocol):
    def __init__(
        self,
        submission_service: ReadingSubmissionService,
        temp_probe_device_id: Optional[int] = None,
    ):
        # Installed modules
        self.temp_probe = TempProbe()
        self.rpi_device = RPIDevice(
            submission_service=submission_service,
            device_module_id=None,
            cpu_module_id=None,
        )
        self.submission_delay = TIME_TO_SLEEP

        # FIXME: Part of the migration of submission service out of the probe driver
        self.submission_service = submission_service
        self.temp_probe_device_id = temp_probe_device_id

    def stop(self):
        # FIXKE: This should be a threading event, to break when the execution is terminated, prevents leaving threads behind
        return False

    def startup(self):
        self.rpi_device.submit_device_startup()

    def run(self):
        while not self.stop():
            # TODO: Would be nice to be able to bundle multiple calls into 1, less of an issue initially
            self.submit_reading()
            self.rpi_device.submit_reading()

            time.sleep(self.submission_delay)

    def shutdown(self):
        self.rpi_device.submit_device_shutdown()

    def get_reading(self) -> bytes:
        """
        Useful for collecting many readings from different modules, rather than submitting all
        at once
        """
        return self.temp_probe.read_temp()

    def submit_reading(self) -> requests.Response:
        """
        Submits a reading to an external endpoint

        :return:
        """
        probe_1_temp = self.get_reading()

        # FIXME: Should this be a float or a string? Broke the test
        data = {"temperature": str(probe_1_temp)}

        response = self.submission_service.submit(
            device_module_id=self.temp_probe_device_id, data=data
        )

        return response


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
