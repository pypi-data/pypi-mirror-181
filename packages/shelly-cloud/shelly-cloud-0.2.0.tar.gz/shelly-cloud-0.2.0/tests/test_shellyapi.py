"""Test cases for the shelly api module"""
from unittest import mock
import pytest

from shellyapi.shellyapi import ShellyApi


DEVICE_REQUEST_RESPONSE = {
    "isok": True,
    "data": {
        "online": False,
        "device_status": {"total_power": -2500, "serial": 1000},
    },
}

DEVICES_REQUEST_RESPONSE = {
    "isok": True,
    "data": {
        "devices_status": {
            "bcff4dfd1c9b": {"total_power": -2500, "serial": 1000},
            "34945474b5ab": {"total_power": -3000, "serial": 1001},
            "4022d8891390": {
                "serial": 22000,
                "meters": [{"power": 10, "total": 30}],
                "relays": [{"ison": True}],
            },
        },
    },
}

DEVICES_IDS = ["bcff4dfd1c9b", "34945474b5ab", "4022d8891390"]

PLUG_S_TURN_RESPONSE = {"isok": True, "data": {"device_id": "4022d8891390"}}

# pylint: disable=unused-argument
def mocked_requests_get(*args, **kwargs):
    """Module handling mocked API requests"""

    # pylint: disable=too-few-public-methods
    class MockResponse:
        """Class handling mocked API responses"""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Return data as a JSON"""
            return self.json_data

    if args[0] == "http://localhost:3000/device/status":
        return MockResponse(DEVICE_REQUEST_RESPONSE, 200)

    if args[0] == "http://localhost:3000/device/all_status":
        return MockResponse(DEVICES_REQUEST_RESPONSE, 200)

    if args[0] == "http://localhost:3000/device/relay/control":
        return MockResponse(PLUG_S_TURN_RESPONSE, 200)

    if args[0] == "http://localhost:3001/device/all_status":
        return MockResponse(None, 200)

    return MockResponse(None, 404)


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_device() -> None:
    """Test if the device of the given ID is returned"""
    api = ShellyApi("http://localhost:3000", "TOKEN")
    assert api.get_device("bcff4dfd1c9b") == DEVICE_REQUEST_RESPONSE


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_all_devices() -> None:
    """Test if all devices are returned"""
    api = ShellyApi("http://localhost:3000", "TOKEN")
    assert api.get_all_devices() == DEVICES_REQUEST_RESPONSE


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_device_ids() -> None:
    """Test if all device ids are returned"""
    api = ShellyApi("http://localhost:3000", "TOKEN")
    assert api.get_device_ids() == DEVICES_IDS


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_turn_on() -> None:
    """Test if a device can be turned on"""
    api = ShellyApi("http://localhost:3000", "TOKEN")
    assert api.plug_s_turn_on(0, "4022d8891390") == PLUG_S_TURN_RESPONSE


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_turn_off() -> None:
    """Test if a device can be turned off"""
    api = ShellyApi("http://localhost:3000", "TOKEN")
    assert api.plug_s_turn_off(0, "4022d8891390") == PLUG_S_TURN_RESPONSE


@mock.patch(
    "requests.post",
    mock.Mock(side_effect=mocked_requests_get),
)
def test_request_status_error() -> None:
    """Test if API call fails"""
    api = ShellyApi("http://localhost:3001", "TOKEN")
    with pytest.raises(Exception) as exception:
        api.get_device_ids()
    assert str(exception.value) == "Request failed with: None"
