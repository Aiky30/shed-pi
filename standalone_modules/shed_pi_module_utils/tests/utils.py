import requests

from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)


class FakeModule:
    def __init__(
        self, submission_service: ReadingSubmissionService, device_module_id: int
    ):
        self.device_module_id = device_module_id
        self.submission_service = submission_service

    def read_fake_data(self):
        return

    def submit_reading(self) -> requests.Response:
        """
        Submits a reading to an external endpoint

        :return: The response
        """
        reading = self.read_fake_data()

        data = {"temperature": str(reading)}

        response = self.submission_service.submit(
            device_module_id=self.device_module_id, data=data
        )

        return response
