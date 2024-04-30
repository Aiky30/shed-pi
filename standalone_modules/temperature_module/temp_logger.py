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

MODULE_POWER_ID = ""
MODULE_TEMP_ID = ""
MODULE_PROBE_TEMP_ID = ""


def check_os():
    return os.uname()[4].startswith("arm")


def get_time():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%H:%M:%S")  # 24-Hour:Minute:Second
    return current_time


class TempProbe:
    def __init__(self):
        self.device_id: int = MODULE_PROBE_TEMP_ID
        # TODO: Make this an env var, it can then be overridden by the tests
        self.base_url: str = HUB_ADDRESS
        self.module_reading_endpoint: str = "/api/v1/device-module-readings/"

        base_dir = "/sys/bus/w1/devices/"
        device_folder = Path.glob(base_dir + "28*")[0]
        self.device_file = device_folder + "/w1_slave"

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

        logger.info(f"Submitting reading: {probe_1_temp}")

        # Get a request client
        # FIXME: Should this be a float or a string? Broke the test
        data = {"temperature": str(probe_1_temp)}
        endpoint = f"{self.base_url}{self.module_reading_endpoint}"
        response = requests.post(
            endpoint,
            data={"device_module": self.device_id, "data": json.dumps(data)},
        )

        # TODO: Validate the response

        return response


class RPIDevice:
    def __init__(self):
        self.device_id = MODULE_POWER_ID
        self.cpu_module_id = MODULE_TEMP_ID

    def get_cpu_temp(self):
        cpu_temp = os.popen("vcgencmd measure_temp").readline()

        # Convert the temp read from the OS to a clean float
        return float(cpu_temp.replace("temp=", "").replace("'C\n", ""))


def main():
    logger.info(f"Shed pi started: {get_time()}, using version: 0.0.1")

    if not check_os():
        logger.error("only rasbian os supported")
        return

    temp_probe = TempProbe()
    rpi_device = RPIDevice()

    while True:
        pi_temp = rpi_device.get_cpu_temp()

        logger.info(f"Pi temp: {pi_temp}")

        temp_probe.submit_reading()

        time.sleep(TIME_TO_SLEEP)


if __name__ == "__main__":
    main()
