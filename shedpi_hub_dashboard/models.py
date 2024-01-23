import uuid
from django.db import models
from django.db.models import JSONField

from shedpi_hub_dashboard.forms.fields import PrettyJsonFormField


class PrettySONField(JSONField):
    def formfield(self, **kwargs):
        defaults = {"form_class": PrettyJsonFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


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
    schema = PrettySONField(null=True, blank=True)

    def __str__(self):
        return self.name


class DeviceModuleReading(models.Model):
    device_module = models.ForeignKey(
        DeviceModule,
        on_delete=models.CASCADE,
        help_text="A device whose readings were collected.",
    )
    data = PrettySONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
