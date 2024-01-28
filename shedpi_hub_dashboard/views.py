from django.template.response import TemplateResponse
from rest_framework import viewsets

from .models import DeviceModule, DeviceModuleReading
from .serlializers import DeviceModuleReadingSerializer, DeviceModuleSerializer


def index(request):
    response = TemplateResponse(request, "shedpi_hub_dashboard/index.html", {})
    return response


class DeviceModuleViewSet(viewsets.ModelViewSet):
    queryset = DeviceModule.objects.all()
    serializer_class = DeviceModuleSerializer


class DeviceModuleReadingViewSet(viewsets.ModelViewSet):
    queryset = DeviceModuleReading.objects.all()
    serializer_class = DeviceModuleReadingSerializer
