from django.template.response import TemplateResponse
from rest_framework import viewsets

from .models import DeviceModuleReading
from .serlializers import DeviceModuleReadingSerializer


def index(request):
    response = TemplateResponse(request, "shedpi_hub_dashboard/index.html", {})
    return response


class DeviceModuleReadingViewSet(viewsets.ModelViewSet):
    queryset = DeviceModuleReading.objects.all()
    serializer_class = DeviceModuleReadingSerializer
