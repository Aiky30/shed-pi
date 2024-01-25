from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from shedpi_hub_dashboard.views import DeviceModuleReadingViewSet

router = routers.DefaultRouter()
router.register(r"device-module-readings", DeviceModuleReadingViewSet)

urlpatterns = [
    *[
        path("admin/", admin.site.urls),
        path("", include("shedpi_hub_dashboard.urls")),
        path("api-auth/", include("rest_framework.urls")),
        path("api/v1/", include(router.urls)),
    ],
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
