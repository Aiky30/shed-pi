from unittest.mock import Mock

from shedpi_hub_dashboard.field_engine import FieldEngine, ValidationErrors

# import pytest

def test_config_engine():
    example_data = [
        {"temp_1": "", "temp_2": "",},
    ]
    specifiction = {
        "fields": {
            "temp_1": {
                "required": False,
                "rules": [
                    {
                        "type": "not_null"
                    }
                ]
            },
            "temp_2": {
                "required": True,
                "rules": []
            }
        }
    }

    engine = FieldEngine(specifiction)

    engine.validate(example_data)

    assert "Field temp_1 failed rule: not_null" in engine.validator.errors.field_errors

    example_data = [
        {},
    ]

    engine = FieldEngine(specifiction)

    engine.validate(example_data)

    assert engine.validator.errors == ValidationErrors(field_errors=[
        "Fields list[{'temp_2'}] are missing"
    ])



