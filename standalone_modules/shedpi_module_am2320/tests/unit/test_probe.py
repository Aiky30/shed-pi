from unittest.mock import Mock, patch

from standalone_modules.shedpi_module_am2320.device_protocol import (
    DeviceProtocol,
)


@patch.object(
    DeviceProtocol,
    "_import_libraries",
)
def test_probe_reading__happy_path(mocked_am2320):
    mocked_submission_service = Mock()
    probe = DeviceProtocol(
        device_module_id=99, submission_service=mocked_submission_service
    )
    mocked_component = Mock(
        temperature=20.0,
        relative_humidity=70.0,
    )
    probe.component = mocked_component

    probe.read_data()

    mocked_submission_service.submit.assert_called_with(
        device_module_id=99, data={"temperature": 20.0, "humidity": 70.0}
    )


@patch.object(
    DeviceProtocol,
    "_import_libraries",
)
def test_probe_reading__missing_data(mocked_am2320):
    mocked_submission_service = Mock()
    probe = DeviceProtocol(
        device_module_id=99, submission_service=mocked_submission_service
    )
    mocked_component = Mock(
        temperature=None,
        relative_humidity=None,
    )
    probe.component = mocked_component

    probe.read_data()

    mocked_submission_service.submit.assert_called_with(
        device_module_id=99, data={"temperature": None, "humidity": None}
    )
