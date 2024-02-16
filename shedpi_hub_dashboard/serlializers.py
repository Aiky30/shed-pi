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
        # extra_kwargs = {"device_module": {"required": True}}
