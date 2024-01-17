import uuid
from django.db import models


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# TODO: Create a Json configurable engine for storage and retrieval
class DeviceReading(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        help_text="A device whose readings were collected.",
    )
    device_temp = models.CharField(max_length=8)
    probe_temp = models.CharField(max_length=8)
