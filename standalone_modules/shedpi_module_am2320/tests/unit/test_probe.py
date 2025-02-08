from unittest.mock import Mock, patch

import pytest

from standalone_modules.shedpi_module_am2320.device_protocol import (
    DeviceProtocol,
)


@patch("standalone_modules.shedpi_module_am2320.device_protocol.AM2320")
def test_probe_reading_no_reading(mocked_am2320):
    mocked_submission_service = Mock()
    probe = DeviceProtocol(submission_service=mocked_submission_service)

    with pytest.raises(ValueError) as err:
        probe.read_data()

    assert err.value.args[0] == "First two read bytes are a mismatch"


#
#
# @patch("shedpi_components.AM2302.posix")
# @patch("shedpi_components.AM2302.ioctl")
# def test_probe_reading_happy_path(mocked_posix, mocked_ioctl):
#     probe = AM2320()
#     # probe.read_temp_raw = Mock(
#     #     return_value=[
#     #         "YES",
#     #         "t=12345",
#     #     ]
#     # )
#
#     mocked_posix.read = Mock(return_value="0000000")
#     probe.read_sensor()
