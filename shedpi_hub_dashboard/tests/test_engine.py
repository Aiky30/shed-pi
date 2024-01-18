from unittest.mock import Mock

from shedpi_hub_dashboard.field_engine import FieldEngine

# import pytest

def test_config_engine():
    example_data = [
        {"temp": ""},
    ]
    rules = {
        "fields": [
            {
                "temp": {
                    "required": True
                }
            }
        ]
    }

    engine = FieldEngine(rules, example_data)

    engine.validate(example_data)

    assert engine.errors is None

    example_data = [
        {},
    ]

    engine = FieldEngine(example_data)

    engine.validate(example_data)

    assert engine.errors is None



