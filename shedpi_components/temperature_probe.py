import time
from pathlib import Path
from typing import Optional

import requests

from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)

# TODO: Remove the submission_service from the component, it's an anti pattern


class TempProbe:
    def __init__(self, submission_service: ReadingSubmissionService):
        self.device_id: int = None
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
