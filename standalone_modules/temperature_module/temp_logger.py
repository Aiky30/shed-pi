import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

"""
TODO:
- Separate installation script
- Requests library
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

HUB_ADDRESS = "http://localhost:8000"
# HUB_ADDRESS = "http://192.168.2.130:8000"

MODULE_VERSION = "0.0.1"
MODULE_POWER_ID = ""
MODULE_TEMP_ID = ""
MODULE_PROBE_TEMP_ID = ""


def check_os():
    return os.uname()[4].startswith("arm")


def get_time():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%H:%M:%S")  # 24-Hour:Minute:Second
    return current_time


class ReadingSubmissionService:
    def __init__(self):
        self.base_url: str = HUB_ADDRESS
        self.data_submission_endpoint: str = "/api/v1/device-module-readings/"

    def submit(self, device_module_id: int, data: dict) -> requests.Response:
        """
        Submit a reading to the ShedPi data submittion endpoint

        :param device_module_id: The DeviceModule id
        :param data: A data payload to submit
        :return:
        """
        logger.info(f"Submitting reading for device: {device_module_id}, {data}")

        endpoint = f"{self.base_url}{self.data_submission_endpoint}"
        response = requests.post(
            endpoint,
            data={"device_module": device_module_id, "data": json.dumps(data)},
        )

        # TODO: Validate the response

        return response


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


class RPIDevice:
    def __init__(self, submission_service: ReadingSubmissionService):
        self.device_id: int = MODULE_POWER_ID
        self.cpu_module_id: int = MODULE_TEMP_ID
        self.submission_service = submission_service

    def get_cpu_temp(self):
        cpu_temp = os.popen("vcgencmd measure_temp").readline()

        # Convert the temp read from the OS to a clean float
        return float(cpu_temp.replace("temp=", "").replace("'C\n", ""))

    def submit_reading(self) -> requests.Response:
        """
        Submits a reading to an external endpoint

        :return:
        """
        cpu_temp = self.get_cpu_temp()

        # FIXME: Should this be a float or a string? Broke the test
        data = {"temperature": str(cpu_temp)}

        response = self.submission_service.submit(device_id=self.device_id, data=data)

        return response

    def submit_device_startup(self):
        logger.info(f"Shed pi started: {get_time()}, using version: {MODULE_VERSION}")

        data = {"power": True}
        response = self.submission_service.submit(device_id=self.device_id, data=data)
        return response

    def submit_device_shutdown(self):
        data = {"power": False}
        response = self.submission_service.submit(device_id=self.device_id, data=data)
        return response


class DeviceProtocol:
    def __init__(self, submission_service: ReadingSubmissionService):
        # Installed modules
        submission_service = ReadingSubmissionService()
        self.temp_probe = TempProbe(submission_service=submission_service)
        self.rpi_device = RPIDevice(submission_service=submission_service)

    def startup(self):
        self.rpi_device.submit_device_startup()

    def run(self):
        while True:
            # TODO: Would be nice to be able to bundle multiple calls into 1, less of an issue initially
            self.temp_probe.submit_reading()
            self.rpi_device.submit_reading()

            time.sleep(TIME_TO_SLEEP)

    def shutdown(self):
        self.rpi_device.submit_device_shutdown()


def main():
    if not check_os():
        logger.error("only rasbian os supported")
        return

    device = DeviceProtocol()

    try:
        device.startup()
        device.run()
    finally:
        device.shutdown()


if __name__ == "__main__":
    main()
