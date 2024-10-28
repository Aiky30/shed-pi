from django.template.response import TemplateResponse
from rest_framework import viewsets

from .models import DeviceModule, DeviceModuleReading
from .serlializers import DeviceModuleReadingSerializer, DeviceModuleSerializer


def index(request):
    response = TemplateResponse(
        request, "shedpi_hub_dashboard/templates/index.html", {}
    )
    return response


def reading(request):
    response = TemplateResponse(
        request, "shedpi_hub_dashboard/templates/reading.html", {}
    )
    return response


class DeviceModuleViewSet(viewsets.ModelViewSet):
    queryset = DeviceModule.objects.all()
    serializer_class = DeviceModuleSerializer


class DeviceModuleReadingViewSet(viewsets.ModelViewSet):
    queryset = DeviceModuleReading.objects.all()
    serializer_class = DeviceModuleReadingSerializer

    def get_queryset(self):
        # FIXME: Validate that the user supplied the get params!
        device_module_id = self.request.query_params.get("device_module")
        start_date = self.request.query_params.get("start")
        end_date = self.request.query_params.get("end")

        if start_date and end_date and device_module_id:
            return self.queryset.filter(
                device_module=device_module_id,
                created_at__date__range=(start_date, end_date),
            )

        elif device_module_id:
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
