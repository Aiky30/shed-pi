import logging
import os
from datetime import datetime, timezone


def check_arch_is_arm() -> bool:
    """
    Is the system architecture an arm?

    :return: True if the Architecture of the device is ARM
    """
    return os.uname()[4].startswith("arm")


def get_time():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%H:%M:%S")  # 24-Hour:Minute:Second
    return current_time


logging.basicConfig(
    filename="/var/log/shed-pi.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)
logger = logging.getLogger("parent")
