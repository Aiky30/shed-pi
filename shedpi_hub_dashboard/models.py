import uuid

from django.db import models
from jsonschema import validate

from shedpi_hub_dashboard.forms.fields import PrettyJsonField


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DeviceModule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        help_text="A device which manages the module.",
    )
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    schema = PrettyJsonField(null=True, blank=True)

    def __str__(self):
        return self.name


class DeviceModuleReading(models.Model):
    device_module = models.ForeignKey(
        DeviceModule,
        on_delete=models.CASCADE,
        help_text="A device whose readings were collected.",
    )
    data = PrettyJsonField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def validate_data(self) -> None:
        """
        Validates the data against the schema defined in the DeviceModule,
        the purpose is to ensure that the data stored matches the data structure expected
        """
        schema = self.device_module.schema

        # Only validate if a schema exists
        if schema:
            validate(
                instance=self.data,
                schema=schema,
            )

    def save(self, *args, **kwargs) -> None:
        """
        On save validates
        """
        self.validate_data()

        super().save(*args, **kwargs)
