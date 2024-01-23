from django.contrib import admin

from .models import Device, DeviceReading


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(DeviceReading)
class DeviceReadingAdmin(admin.ModelAdmin):
    pass
