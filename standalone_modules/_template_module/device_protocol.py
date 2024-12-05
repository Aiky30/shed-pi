from standalone_modules.shed_pi_module_utils.base_protocol import BaseProtocol
from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from standalone_modules.shed_pi_module_utils.utils import logger


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        ...

    def stop(self):
        logger.info("Stopping device protocol")

    def start(self):
        logger.info("Starting device protocol")


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
