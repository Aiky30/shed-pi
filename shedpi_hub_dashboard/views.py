from django.template.response import TemplateResponse
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from .models import DeviceModule, DeviceModuleReading
from .pagination import CreatedAtBasedCursorPagination
from .serlializers import (
    DeviceModuleReadingListSerializer,
    DeviceModuleReadingSerializer,
    DeviceModuleSerializer,
)


def index(request):
    response = TemplateResponse(request, "shedpi_hub_dashboard/index.html", {})
    return response


class DeviceModuleViewSet(viewsets.ModelViewSet):
    queryset = DeviceModule.objects.all()
    serializer_class = DeviceModuleSerializer


class DeviceModuleReadingViewSet(viewsets.ModelViewSet):
    queryset = DeviceModuleReading.objects.all()
    serializer_class = DeviceModuleReadingSerializer

    def get_serializer_class(self):
        if hasattr(self, "action") and self.action == "list":
            return DeviceModuleReadingListSerializer
        return DeviceModuleReadingSerializer

    def get_queryset(self):
        # FIXME: Validate that the user supplied this get param!
        device_module_id = self.request.query_params.get("device_module")

        if device_module_id:
            return self.queryset.filter(device_module=device_module_id)

        return self.queryset


class ExperimentalViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = DeviceModuleReading.objects.all()
    serializer_class = DeviceModuleReadingListSerializer
    pagination_class = CreatedAtBasedCursorPagination

    def get_queryset(self):
        # FIXME: Validate that the user supplied this get param!
        device_module_id = self.request.query_params.get("device_module")

        if device_module_id:
            return self.queryset.filter(device_module=device_module_id)

        return self.queryset
