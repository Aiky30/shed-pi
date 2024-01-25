# TODO:
# - Schema with data fields
# - Submit data to the endpoints
import pytest
from django.urls import reverse
from rest_framework import status

from shedpi_hub_dashboard.tests.utils.factories import DeviceModuleFactory


@pytest.mark.django_db
def test_device_reading_submission(client):
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person",
        "type": "object",
        "properties": {
            "temperature": {"type": "string", "description": "The Temperature"},
        },
    }
    device_module = DeviceModuleFactory(schema=schema)
    # devicemodulereading-list
    # devicemodulereading-detail
    url = reverse("devicemodulereading-detail", kwargs={"pk": device_module.id})

    response = client.post(url, data={"device_module_id": device_module.id})

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == {}
