import json
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

HUB_ADDRESS = "http://localhost:8000"
# HUB_ADDRESS = "http://192.168.2.130:8000"


class ReadingSubmissionService:
    def __init__(self, base_url: Optional[str] = HUB_ADDRESS):
        self.base_url = base_url
        self.data_submission_endpoint: str = "/api/v1/device-module-readings/"

    def submit(self, device_module_id: int, data: dict) -> requests.Response:
        """
        Submit a reading to the ShedPi data submission endpoint

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
