import json

import pytest
from rest_framework import status
from shed_pi_module_utils.data_submission import (
    ReadingSubmissionService,
)
from shed_pi_module_utils.tests.utils import FakeModule

from shedpi_hub_dashboard.models import DeviceModuleReading
from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
)


@pytest.mark.django_db
def test_module_reading_submission(live_server):
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Reading",
        "type": "object",
        "properties": {
            "some_prop": {"type": "string", "description": "Fake property"},
        },
    }
    device_module = DeviceModuleFactory(schema=schema)
    submission_service = ReadingSubmissionService(base_url=live_server.url)
    fake_module = FakeModule(
        submission_service=submission_service, device_module_id=device_module.id
    )

    response = fake_module.submit_reading()

    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.text)

    assert "created_at" in response_data
    assert DeviceModuleReading.objects.filter(device_module=device_module).count() == 1
