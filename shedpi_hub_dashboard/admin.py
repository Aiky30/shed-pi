from django.contrib import admin

from .models import Device, DeviceModule, DeviceModuleReading


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class DeviceModuleReadingInlineAdmin(admin.TabularInline):
    model = DeviceModuleReading
    extra = 0
    can_delete = False

    # TODO: trying to limit the inline with pagination
    # list_per_page = 5  # No of records per page
    #
    # def get_queryset(self, request):
    #     # TODO: return type -> QuerySet
    #
    #     queryset = super().get_queryset(request)
    #
    #     return queryset[:5]


@admin.register(DeviceModule)
class DeviceModuleAdmin(admin.ModelAdmin):
    inlines: list = [DeviceModuleReadingInlineAdmin]


@admin.register(DeviceModuleReading)
class DeviceModuleReadingAdmin(admin.ModelAdmin):
    list_display = ("id", "device_module_id", "created_at")
    list_filter = ("device_module_id",)
