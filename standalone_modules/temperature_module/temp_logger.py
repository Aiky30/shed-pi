import logging
import time
from pathlib import Path
from typing import Optional

import requests

from standalone_modules.rpi.device import RPIDevice
from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from standalone_modules.shed_pi_module_utils.utils import check_arch_is_arm

"""
TODO:
- Separate installation script
- Login and push
- Power on is actually Application start!
"""


logging.basicConfig(
    filename="/var/log/shed-pi.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)
logger = logging.getLogger("parent")

TIME_TO_SLEEP = 60  # time in seconds


MODULE_POWER_ID = ""
MODULE_TEMP_ID = ""
MODULE_PROBE_TEMP_ID = ""


class TempProbe:
    def __init__(self, submission_service: ReadingSubmissionService):
        self.device_id: int = MODULE_PROBE_TEMP_ID
        # TODO: Make this an env var, it can then be overridden by the tests
        base_dir = "/sys/bus/w1/devices/"
        device_folder = Path.glob(base_dir + "28*")[0]
        self.device_file = device_folder + "/w1_slave"
        self.submission_service = submission_service

    def read_temp_raw(self) -> list[str]:
        with open(self.device_file, "r") as f:
            lines = f.readlines()

        f.close()
        return lines

    def is_data_available(self, lines: list) -> bool:
        return lines[0].strip()[-3:] != "YES"

    def read_temp(self) -> Optional[float]:
        lines = self.read_temp_raw()
        while self.is_data_available(lines):
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def submit_reading(self) -> requests.Response:
        """
        Submits a reading to an external endpoint

        :return:
        """
        probe_1_temp = self.read_temp()

        # FIXME: Should this be a float or a string? Broke the test
        data = {"temperature": str(probe_1_temp)}

        response = self.submission_service.submit(
            device_module_id=self.device_id, data=data
        )

        return response


class DeviceProtocol:
    def __init__(self, submission_service: ReadingSubmissionService):
        # Installed modules
        self.temp_probe = TempProbe(submission_service=submission_service)
        self.rpi_device = RPIDevice(
            submission_service=submission_service,
            device_module_id=MODULE_POWER_ID,
            cpu_module_id=MODULE_TEMP_ID,
        )
        self.submission_delay = TIME_TO_SLEEP

    def stop(self):
        return False

    def startup(self):
        self.rpi_device.submit_device_startup()

    def run(self):
        while not self.stop():
            # TODO: Would be nice to be able to bundle multiple calls into 1, less of an issue initially
            self.temp_probe.submit_reading()
            self.rpi_device.submit_reading()

            time.sleep(self.submission_delay)

    def shutdown(self):
        self.rpi_device.submit_device_shutdown()


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
