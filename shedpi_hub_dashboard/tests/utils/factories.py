from uuid import uuid4

import factory
from factory.django import DjangoModelFactory

from shedpi_hub_dashboard.models import Device, DeviceModule, DeviceModuleReading


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Faker("word")
    location = factory.Faker("word")


class DeviceModuleFactory(DjangoModelFactory):
    class Meta:
        model = DeviceModule

    id = factory.LazyFunction(lambda: str(uuid4()))
    device = factory.SubFactory(DeviceFactory)
    name = factory.Faker("word")
    location = factory.Faker("word")
    schema = {}


class DeviceModuleReadingFactory(DjangoModelFactory):
    class Meta:
        model = DeviceModuleReading

    device_module = factory.SubFactory(DeviceModuleFactory)
    data = {}
