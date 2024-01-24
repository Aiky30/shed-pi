import pytest
from jsonschema.exceptions import SchemaError, ValidationError

from shedpi_hub_dashboard.models import DeviceModuleReading
from shedpi_hub_dashboard.tests.utils.factories import DeviceModuleFactory

"""
device_temp = models.CharField(max_length=8)
    probe_temp = models.CharField(max_length=8)
    measurement_type = models.CharField(max_length=10)

TODO:
    # Design where the validation shoudl live, needs to:
    # '- Validate on save
    # - Validate on Restful save / edit
"""


@pytest.mark.django_db
def test_schema_validation_happy_path():
    """
    The data validation should succeed when the schema is valid
    """
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person",
        "type": "object",
        "properties": {
            "firstName": {"type": "string", "description": "The person's first name."},
            "lastName": {"type": "string", "description": "The person's last name."},
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0,
            },
        },
    }
    data = {"firstName": "John", "lastName": "Doe", "age": 21}
    device_module = DeviceModuleFactory(schema=schema)

    reading = DeviceModuleReading(device_module=device_module, data=data)

    # By default no validation error is raised
    reading.save()


@pytest.mark.django_db
def test_json_schema_invalid_data():
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person",
        "type": "object",
        "properties": {
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0,
            }
        },
    }
    data = {"age": 21}
    updated_data = {"age": "Some text"}
    device_module = DeviceModuleFactory(schema=schema)
    reading = DeviceModuleReading(device_module=device_module, data=data)

    # No error occurs with valid data
    reading.save()

    # With invalid data it now throws a validation error
    with pytest.raises(ValidationError):
        reading.data = updated_data
        reading.save()


@pytest.mark.django_db
def test_json_schema_update_with_invalid_data():
    schema = {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person",
        "type": "object",
        "properties": {
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0,
            }
        },
    }
    data = {"age": "Some text"}
    device_module = DeviceModuleFactory(schema=schema)
    reading = DeviceModuleReading(device_module=device_module, data=data)

    with pytest.raises(ValidationError):
        reading.save()


@pytest.mark.django_db
def test_json_schema_invalid_schema():
    schema = {"type": 1234}
    data = {"firstName": "John", "lastName": "Doe", "age": 21}

    device_module = DeviceModuleFactory(schema=schema)
    reading = DeviceModuleReading(device_module=device_module, data=data)

    with pytest.raises(SchemaError):
        reading.save()
