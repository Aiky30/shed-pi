import json
from unittest.mock import Mock, patch

import pytest
from rest_framework import status

from shedpi_hub_dashboard.models import DeviceModuleReading
from shedpi_hub_dashboard.tests.utils.factories import (
    DeviceModuleFactory,
)

from .temp_logger import TempProbe


@patch("standalone_modules.temperature_module.temp_logger.Path")
def test_temp_probe_reading_happy_path(mocked_path):
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


# Integration test, TODO: Move to Integration folder
@patch("standalone_modules.temperature_module.temp_logger.Path")
@pytest.mark.django_db
def test_temperature_module_reading_submission(mocked_path, live_server):
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

    probe = TempProbe()
    probe.device_id = device_module.id
    probe.base_url = live_server.url
    probe.read_temp_raw = Mock(
        return_value=[
            "YES",
            "t=12345",
        ]
    )

    response = probe.submit_reading()

    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.text)

    # assert response_data

    assert DeviceModuleReading.objects.filter(device_module=device_module).count() == 1


# TODO: Test default endpoint address settings work in theory, because the test above overrides them
