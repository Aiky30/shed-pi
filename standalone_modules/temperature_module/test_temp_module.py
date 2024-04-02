from unittest.mock import Mock, patch

import pytest
from django.urls import reverse

from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
)

from .temp_logger import TempProbe


@patch("standalone_modules.temperature_module.temp_logger.Path")
def test_temp_probe_reading_happy_path(mocked_path):
    """
    TODO:
    - Mock rpi
    - Mock device output
    - Test the case for YES from the module
    """
    # FIXME: Get the actual readout from the modules
    probe = TempProbe()
    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=12345",
        ]
    )
    temp = probe.read_temp()

    assert temp == 12.345


@patch("standalone_modules.temperature_module.temp_logger.Path")
def test_temp_probe_reading_invalid_reading(mocked_path):
    """
    TODO:
    - Find what a real invalid reading looks like
    """
    # FIXME: Get the actual readout from the modules
    probe = TempProbe()
    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=xxxxxx",
        ]
    )

    with pytest.raises(ValueError):
        probe.read_temp()


@patch("standalone_modules.temperature_module.temp_logger.Path")
def test_temp_probe_reading_invalid_reading_missing_expected_params(mocked_path):
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
    probe = TempProbe()
    probe.read_temp_raw = Mock(side_effect=[try_1, try_2])

    temp = probe.read_temp()

    assert temp == 2.0
    # The first reading is discarded as invalid
    probe.read_temp_raw.call_count == 2


@pytest.mark.django_db
def test_temperature_module_reading_submission(client):
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

    # The below is what the module will recieve and we will be able to see that it has somehow
    # response = client.post(
    #     url, data={"device_module": device_module.id, "data": json.dumps(data)}
    # )
    #
    # assert response.status_code == status.HTTP_201_CREATED
    # assert response.data["data"] == data
