from rest_framework import serializers

from .models import DeviceModuleReading


class DeviceModuleReadingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceModuleReading
        fields = "__all__"
