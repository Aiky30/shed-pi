import uuid
from django.db import models


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DeviceReading(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        help_text="A device whose readings were collected.",
    )
    # TODO: Create a Json configurable engine for storage and retrieval fields¬
    device_temp = models.CharField(max_length=8)
    probe_temp = models.CharField(max_length=8)
    measurement_type = models.CharField(max_length=10)
    datetime = models.DateTimeField()
