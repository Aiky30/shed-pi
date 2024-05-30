from typing import Optional

from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from shedpi_hub_dashboard.models import Device, DeviceModule, DeviceModuleReading

# TODO: Logger

"""
A script ot import the data that has already been gathered

Historic data structure:
    "Shed pi started: {get_time()}, using version: 0.0.1"
    "Pi temp: {pi_temp}, probe_1 temp: {probe_1_temp}"

FIXME:
    Allow the data submission endpoint to take multiple device modules and readings.
    Example: Pi has it's own data and so does the temp probe. More effecient to send at once

TODO:
    Module code
        - Need a device module for PI temp amd Probe temp, with working api connection
        - Call api endpoints to store
            - probe temp
            - device tenp
            - device on / off (ignore datetime from the device which will be wrong on startup)
    Hub code
        - Need the ability to be able to create an action for device on off

    django admin device_module_readings: filter by device_module,
        could be seriously heavy query, separate ticket for perf

    Allow multiple imports of different modules from the same api endpoint (low priority, greener, less traffic)

"""


class FileImport:
    def __init__(self, file_path: str):
        # Create Temp module

        self.device_pi_temp_module: Optional[DeviceModule] = None
        self.device_probe_temp_module: Optional[DeviceModule] = None
        self.device_pi_power_module: Optional[DeviceModule] = None

        self.file_path = file_path
        self.data_map: list = []

    def _set_device_module(self) -> None:
        """
        If a device or device module already exists, error and fall over, we have already imported this data.
        This gets around the issue of not being able to handle multiple inserts
        """
        device, device_created = Device.objects.get_or_create(
            name="Hub",
            location="garage",
        )

        if not device_created:
            raise IntegrityError("Device already exists")

        (
            self.device_pi_power_module,
            pi_power_device_module_created,
        ) = DeviceModule.objects.get_or_create(
            device=device,
            name="Device power",
            location="Garage",
            schema={
                "$id": "https://example.com/person.schema.json",
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "properties": {
                    "power": {
                        "description": "The Hub power state",
                        "type": "boolean",
                    }
                },
                "title": "Reading",
                "type": "object",
            },
        )
        if not pi_power_device_module_created:
            raise IntegrityError(
                f"Device Module {self.device_pi_power_module} already exists"
            )

        (
            self.device_pi_temp_module,
            pi_temp_device_module_created,
        ) = DeviceModule.objects.get_or_create(
            device=device,
            name="Device temperature",
            location="Garage",
            schema={
                "$id": "https://example.com/person.schema.json",
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "properties": {
                    "temperature": {
                        "description": "The Hub device temperature",
                        "type": "string",
                    }
                },
                "title": "Reading",
                "type": "object",
            },
        )
        if not pi_temp_device_module_created:
            raise IntegrityError(
                f"Device Module {self.device_pi_temp_module} already exists"
            )

        (
            self.device_probe_temp_module,
            probe_device_module_created,
        ) = DeviceModule.objects.get_or_create(
            device=device,
            name="Temperature probe",
            location="Garage low",
            schema={
                "$id": "https://example.com/person.schema.json",
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "properties": {
                    "temperature": {
                        "description": "The temperature probe reading",
                        "type": "string",
                    }
                },
                "title": "Reading",
                "type": "object",
            },
        )

        if not probe_device_module_created:
            raise IntegrityError(
                f"Device Module {self.device_probe_temp_module} already exists"
            )

    def _process_file_line(self, line: str):
        log_parts = line.split(":INFO:parent:")
        # Timestamp contained some crazy characters for the power on and off logs
        log_timestamp = log_parts[0].lstrip("\x00")
        log_message = log_parts[1]

        # Handle started at message
        if log_message.startswith("Shed pi started: "):
            # Need a way to be able to record events, such as the device turning on / off

            self.data_map.append(
                DeviceModuleReading(
                    device_module=self.device_pi_power_module,
                    created_at=log_timestamp,
                    data={"power": True},
                )
            )
            return

        elif log_message.startswith("Pi temp: "):
            temps = log_message.split(": ")

            pi_temp: str = ""
            probe_temp: Optional[str] = None

            if len(temps) > 2:
                assert temps[0] == "Pi temp"
                # Splti the next reading into 2
                partial_reading = temps[1].split(",")
                assert partial_reading[1] == " probe_1 temp"

                pi_temp = partial_reading[0]
                probe_temp = temps[2].strip()
            else:
                assert temps[0] == "Pi temp"
                pi_temp = temps[1].strip()

            self.data_map.append(
                DeviceModuleReading(
                    device_module=self.device_pi_temp_module,
                    created_at=log_timestamp,
                    data={"temperature": pi_temp},
                )
            )

            if probe_temp:
                self.data_map.append(
                    DeviceModuleReading(
                        device_module=self.device_probe_temp_module,
                        created_at=log_timestamp,
                        data={"temperature": probe_temp},
                    )
                )

            # TODO: The temp should be stored and validated as a float, Schema rule!!
            # DeviceModuleReading.objects.aget_or_create(
            #     device_module=self.import_module,
            #     created_at=log_timestamp,
            #     data={"temperature": pi_temp},
            # )

            print("checking for import")

    def _processed_mapped_data(self):
        # TODO: Look to see if the data exists in the DB, what would this look like?
        # https://gist.github.com/dorosch/6cffd2936ac05ef8794c82901ab4d6e7

        print(f"count pre run: {DeviceModuleReading.objects.all().count()}")
        DeviceModuleReading.objects.bulk_create(self.data_map, ignore_conflicts=True)
        print(f"count post run: {DeviceModuleReading.objects.all().count()}")

    def _process_file(self) -> None:
        with open(self.file_path, "r") as file_feed:
            for log in file_feed.readlines():
                self._process_file_line(log)

        self._processed_mapped_data()

    @transaction.atomic()
    def import_data(self):
        # FIXME: Add timing logs to help speed this up
        self._set_device_module()

        self._process_file()


class Command(BaseCommand):
    help = "Imports historic data"

    def handle(self, *args, **options):
        self.stdout.write("Started import")

        file_import = FileImport(
            file_path="./historic_data_import/data/shed-pi-2024-04-02.log"
        )
        file_import.import_data()

        self.stdout.write(self.style.SUCCESS("Completed import"))
