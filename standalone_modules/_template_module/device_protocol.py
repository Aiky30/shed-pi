from shed_pi_module_utils import BaseProtocol
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.utils import logger


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        ...

    # Provide a method of getting the data from the device
    # def get_reading():

    # Provide a method to submit the data
    # def submit_reading():
    #   reading = self.get_reading()
    #   submission_service.submit_reading

    def stop(self):
        logger.info("Stopping device protocol")

    def start(self):
        logger.info("Starting device protocol")

        # while True:
        #   self.submit_reading()


def main():
    # The Submission service is used to record any module data
    submission_service = ReadingSubmissionService()
    device = DeviceProtocol(submission_service=submission_service)

    try:
        device.startup()
        device.start()
    finally:
        device.shutdown()


if __name__ == "__main__":
    main()
