from unittest.mock import Mock

import pytest
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.shed_pi_components.ds18b20 import (
    TempProbe,
)

from shedpi_hub_dashboard.models import DeviceModuleReading
from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
)
from standalone_modules.temperature_module.device_protocol import DeviceProtocol


def test_temp_probe_reading_happy_path(temp_probe_path):
    # FIXME: Get the actual readout from the modules
    probe = TempProbe(submission_service=Mock())
    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=12345",
        ]
    )
    temp = probe.read_temp()

    assert temp == 12.345


def test_temp_probe_reading_invalid_reading(temp_probe_path):
    """
    TODO:
    - Find what a real invalid reading looks like
    """
    # FIXME: Get the actual readout from the modules
    probe = TempProbe(submission_service=Mock())
    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=xxxxxx",
        ]
    )

    with pytest.raises(ValueError):
        probe.read_temp()


def test_temp_probe_reading_invalid_reading_missing_expected_params(temp_probe_path):
    """
    YES is missing from the data feed
    """
    # FIXME: Get the actual readout from the modules

    try_1 = [
        "SOMETHING",
        "t=1000",
    ]
    try_2 = [
        "YES",
        "t=2000",
    ]
    probe = TempProbe(submission_service=Mock())
    probe.read_temp_raw = Mock(side_effect=[try_1, try_2])

    temp = probe.read_temp()

    assert temp == 2.0
    # The first reading is discarded as invalid
    probe.read_temp_raw.call_count == 2


@pytest.mark.django_db
def test_temp_logger(temp_probe_path, live_server):
    # Submission service
    submission_service = ReadingSubmissionService()
    submission_service.base_url = live_server.url
    # Device Protocol
    device_protocol = DeviceProtocol(submission_service=submission_service)
    # Override the loop timer for the test to end instantly
    device_protocol.submission_delay = 0
    device_protocol.stop = Mock(side_effect=[False, True])
    # Temp probe
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Reading",
        "type": "object",
        "properties": {
            "temperature": {"type": "string", "description": "The Temperature"},
        },
    }
    temp_probe = DeviceModuleFactory(schema=schema)
    device_protocol.temp_probe.device_id = temp_probe.id
    device_protocol.temp_probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=12345",
        ]
    )

    device_protocol.run()

    # Check that the data was submitted
    assert DeviceModuleReading.objects.filter(device_module=temp_probe).count() == 1
