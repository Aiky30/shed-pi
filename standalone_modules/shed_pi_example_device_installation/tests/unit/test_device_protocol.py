from unittest.mock import Mock, patch

import pytest
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)

from shedpi_hub_dashboard.models import DeviceModuleReading
from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
)
from standalone_modules.shed_pi_example_device_installation.device_protocol import (
    DeviceProtocol,
)


@patch("standalone_modules.temperature_module.temperature_probe.Path")
@pytest.mark.django_db
def test_device_protocol(mocked_path, live_server):
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
    # RPI CPU temp probe
    rpi_schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Reading",
        "type": "object",
        "properties": {
            "temperature": {"type": "string", "description": "The Temperature"},
        },
    }
    rpi_cpu_temp = DeviceModuleFactory(schema=rpi_schema)
    device_protocol.rpi_device.device_module_id = rpi_cpu_temp.id
    device_protocol.rpi_device.get_cpu_temp = Mock(return_value=10.0)

    device_protocol.run()

    # Check that the data was submitted
    assert DeviceModuleReading.objects.filter(device_module=rpi_cpu_temp).count() == 1
    assert DeviceModuleReading.objects.filter(device_module=temp_probe).count() == 1
