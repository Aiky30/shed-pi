from django.contrib import admin

from .models import Device, DeviceModule, DeviceModuleReading


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(DeviceModule)
class DeviceModuleAdmin(admin.ModelAdmin):
    pass

@admin.register(DeviceModuleReading)
class DeviceModuleReadingAdmin(admin.ModelAdmin):
    pass
