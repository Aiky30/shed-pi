from typing import ClassVar

from rest_framework import serializers

from .models import DeviceModule, DeviceModuleReading


class DeviceModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModule
        fields = "__all__"


class DeviceModuleReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModuleReading
        fields = "__all__"
        extra_kwargs: ClassVar[dict] = {"device_module": {"required": True}}


class DeviceModuleReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModuleReading
        exclude: ClassVar[list] = ["device_module"]
