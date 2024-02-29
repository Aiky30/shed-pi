import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
    DeviceModuleReadingFactory,
)


@pytest.mark.django_db
def test_device_module_list(client):
    DeviceModuleFactory.create_batch(2)

    url = reverse("devicemodule-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_device_module_readings_list(client):
    """
    An individual device module readings are returned from the module readings endpoint
    """
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
    DeviceModuleReadingFactory(device_module=device_module, data={"temperature": "20"})
    DeviceModuleReadingFactory(device_module=device_module, data={"temperature": "22"})
    # Another modules readings that shouldn't be returned
    DeviceModuleReadingFactory(data={"temperature": "10"})

    # url = reverse("devicemodulereading-detail", kwargs={"pk": device_module.id})
    url = reverse("devicemodulereading-list")
    response = client.get(url, data={"device_module": device_module.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_device_module_readings_list_pagination(client):
    """
    An individual device module readings are returned from the module readings endpoint
    """
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
    DeviceModuleReadingFactory.create_batch(
        110, device_module=device_module, data={"temperature": "20"}
    )

    url = reverse("devicemodulereading-paginated-list")
    response = client.get(url, data={"device_module": device_module.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 100


@pytest.mark.django_db
def test_device_module_readings_list_no_device_module_supplied(client):
    """ """
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
    DeviceModuleReadingFactory(device_module=device_module, data={"temperature": "20"})
    DeviceModuleReadingFactory(device_module=device_module, data={"temperature": "22"})
    # Another modules readings that shouldn't be returned
    DeviceModuleReadingFactory(data={"temperature": "10"})

    # url = reverse("devicemodulereading-detail", kwargs={"pk": device_module.id})
    url = reverse("devicemodulereading-list")
    response = client.get(url, data={})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


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
