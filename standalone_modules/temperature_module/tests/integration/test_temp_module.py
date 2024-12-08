import json
from unittest.mock import Mock

import pytest
from rest_framework import status
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


@pytest.mark.django_db
def test_temperature_module_reading_submission(temp_probe_path, live_server):
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Reading",
        "type": "object",
        "properties": {
            "temperature": {"type": "string", "description": "The Temperature"},
        },
    }
    device_module = DeviceModuleFactory(schema=schema)
    submission_service = ReadingSubmissionService(base_url=live_server.url)

    probe = TempProbe(submission_service=submission_service)
    # Override the module id
    probe.device_id = device_module.id

    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=12345",
        ]
    )

    response = probe.submit_reading()

    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.text)

    assert "created_at" in response_data
    assert DeviceModuleReading.objects.filter(device_module=device_module).count() == 1
