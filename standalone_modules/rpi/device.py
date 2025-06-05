import logging
import os

import requests
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.utils import get_time

logger = logging.getLogger(__name__)

MODULE_VERSION = "0.0.1"


class RPIDevice:
    def __init__(
        self,
        submission_service: ReadingSubmissionService,
        device_module_id: int,
        cpu_module_id: int,
    ) -> None:
        self.device_module_id = device_module_id
        self.cpu_module_id = cpu_module_id
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

        response = self.submission_service.submit(
            device_module_id=self.device_module_id, data=data
        )

        return response

    def submit_device_startup(self):
        logger.info(f"Shed pi started: {get_time()}, using version: {MODULE_VERSION}")

        data = {"power": True}
        response = self.submission_service.submit(
            device_module_id=self.device_module_id, data=data
        )
        return response

    def submit_device_shutdown(self):
        data = {"power": False}
        response = self.submission_service.submit(
            device_module_id=self.device_module_id, data=data
        )
        return response
