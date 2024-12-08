from unittest.mock import patch

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


# Component Temp probe
@pytest.fixture
def temp_probe_path():
    with patch("shed_pi_module_utils.shed_pi_components.ds18b20.Path"):
        yield
