from unittest.mock import Mock, patch

import pytest

from shedpi_components.AM2302 import AM2320


@patch("shedpi_components.AM2302.posix")
@patch("shedpi_components.AM2302.ioctl")
def test_probe_reading_no_reading(mocked_posix, mocked_ioctl):
    probe = AM2320()

    with pytest.raises(ValueError) as err:
        probe.read_sensor()

    assert err.value.args[0] == "First two read bytes are a mismatch"


@patch("shedpi_components.AM2302.posix")
@patch("shedpi_components.AM2302.ioctl")
def test_probe_reading_happy_path(mocked_posix, mocked_ioctl):
    probe = AM2320()
    # probe.read_temp_raw = Mock(
    #     return_value=[
    #         "YES",
    #         "t=12345",
    #     ]
    # )

    mocked_posix.read = Mock(return_value="0000000")
    reading = probe.read_sensor()
