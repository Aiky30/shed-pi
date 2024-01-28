import json

import pytest
from django.urls import reverse
from rest_framework import status

from shedpi_hub_dashboard.tests.utils.factories import DeviceModuleFactory


@pytest.mark.django_db
def test_device_module_list(client):
    DeviceModuleFactory.create_batch(2)

    url = reverse("devicemodule-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_device_module_reading_submission(client):
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

    # url = reverse("devicemodulereading-detail", kwargs={"pk": device_module.id})
    url = reverse("devicemodulereading-list")
    data = {"temperature": "20.001"}
    response = client.post(
        url, data={"device_module": device_module.id, "data": json.dumps(data)}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["data"] == data
