import time

from standalone_modules.rpi.device import RPIDevice
from standalone_modules.shed_pi_module_utils.base_protocol import BaseProtocol
from standalone_modules.shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from standalone_modules.shed_pi_module_utils.utils import check_arch_is_arm, logger

TIME_TO_SLEEP = 60  # time in seconds


class DeviceProtocol(BaseProtocol):
    def __init__(self, submission_service: ReadingSubmissionService):
        # Installed modules
        self.rpi_device = RPIDevice(
            submission_service=submission_service,
            device_module_id=None,
            cpu_module_id=None,
        )
        self.submission_delay = TIME_TO_SLEEP

    def stop(self):
        return False

    def startup(self):
        self.rpi_device.submit_device_startup()

    def run(self):
        while not self.stop():
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
