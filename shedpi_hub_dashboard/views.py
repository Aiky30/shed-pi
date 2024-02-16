from django.template.response import TemplateResponse
from rest_framework import viewsets

from .models import DeviceModule, DeviceModuleReading
from .pagination import CreatedAtBasedCursorPagination
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
    pagination_class = CreatedAtBasedCursorPagination

    def get_queryset(self):
        # FIXME: Validate that the user supplied this get param!
        device_module_id = self.request.query_params.get("device_module")

        if device_module_id:
            return self.queryset.filter(device_module=device_module_id)

        return self.queryset

    # def list(self, request):
    #     queryset = self.get_queryset()
    #
    #     context = {"request": request}
    #     device_module_id = self.request.query_params.get("device_module")
    #
    #     if device_module_id:
    #         queryset = queryset.filter(device_module=device_module_id)
    #
    #         context["device_module"] = device_module_id
    #
    #     context["queryset"] = queryset
    #
    #     serializer = self.get_serializer(data=request.data, context=context)
    #     serializer.is_valid(raise_exception=True)
    #
    #     return Response(serializer.data)
