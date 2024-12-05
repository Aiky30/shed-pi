from unittest.mock import patch

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


# Component Temp probe
@pytest.fixture
def temp_probe_path():
    with patch("shedpi_components.temperature_probe.Path"):
        yield
