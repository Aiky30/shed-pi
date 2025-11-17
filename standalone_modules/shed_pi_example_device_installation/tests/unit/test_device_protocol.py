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


@pytest.mark.django_db
def test_device_protocol(temp_probe_path, live_server):
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
    # Submission service
    submission_service = ReadingSubmissionService()
    submission_service.base_url = live_server.url
    config = {
        "device": {
            "module_id": "",
        },
        "external_temp": {
            "module_id": temp_probe.id,
        },
        "cpu_temp": {"module_id": rpi_cpu_temp.id},
    }
    with patch.object(DeviceProtocol, "get_config", Mock(return_value=config)):
        # Device Protocol
        device_protocol = DeviceProtocol(submission_service=submission_service)

    # Override the loop timer for the test to end instantly
    # FIXME: This is just a patched sleep!
    device_protocol.submission_delay = 0
    device_protocol.stop = Mock(side_effect=[False, True])
    device_protocol.temp_probe.read_temp = Mock(
        return_value=30.00,
    )
    device_protocol.rpi_device.get_cpu_temp = Mock(return_value=10.0)

    # FIXME: Would be better if we could run for a cycle and exit to prove out the run
    #       method
    device_protocol.submit_reading()
    device_protocol.rpi_device.submit_reading()

    # Check that the data was submitted
    assert DeviceModuleReading.objects.filter(device_module=rpi_cpu_temp).count() == 1
    assert DeviceModuleReading.objects.filter(device_module=temp_probe).count() == 1
