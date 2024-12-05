import time

from shedpi_components.temperature_probe import TempProbe
from standalone_modules.shed_pi_module_utils.base_protocol import BaseProtocol
from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from standalone_modules.shed_pi_module_utils.utils import check_arch_is_arm, logger

TIME_TO_SLEEP = 60  # time in seconds


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        # Installed modules
        self.temp_probe = TempProbe(submission_service=submission_service)
        self.submission_delay = TIME_TO_SLEEP

    def stop(self):
        return False

    def run(self):
        while not self.stop():
            self.temp_probe.submit_reading()

            time.sleep(self.submission_delay)


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
