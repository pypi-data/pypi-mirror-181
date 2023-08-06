"""Client library for interacting with Schlage WiFi locks."""

from __future__ import annotations

import dataclasses
import pycognito
from pycognito.utils import RequestsSrpAuth
import requests
from threading import Lock as Mutex

_API_KEY = "hnuu9jbbJr7MssFDWm5nU2Z7nG5Q5rxsaqWsE7e9"
_BASE_URL = "https://api.allegion.yonomi.cloud/v1/devices/"
_CLIENT_ID = "t5836cptp2s1il0u9lki03j5"
_CLIENT_SECRET = "1kfmt18bgaig51in4j4v1j3jbe7ioqtjhle5o6knqc5dat0tpuvo"
_DEFAULT_TIMEOUT = 60
_USER_POOL_REGION = "us-west-2"
_USER_POOL_ID = _USER_POOL_REGION + "_2zhrVs9d4"


class SchlageAuth:
    """Handles authentication for the Schlage WiFi cloud service."""

    def __init__(self, username: str, password: str) -> None:
        """Initializer."""
        self._auth = RequestsSrpAuth(
            password=password,
            cognito=pycognito.Cognito(
                username=username,
                user_pool_region=_USER_POOL_REGION,
                user_pool_id=_USER_POOL_ID,
                client_id=_CLIENT_ID,
                client_secret=_CLIENT_SECRET,
            ),
        )

    def authenticate(self):
        """Performs authentication with AWS."""
        self._auth()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Performs a request against the cloud service."""
        kwargs["auth"] = self._auth
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["X-Api-Key"] = _API_KEY
        timeout = kwargs.pop("timeout", _DEFAULT_TIMEOUT)
        return requests.request(
            method, f"{_BASE_URL}/{path}", timeout=timeout, **kwargs
        )


@dataclasses.dataclass
class Device:
    """A Schlage WiFi device."""

    _mu: Mutex = dataclasses.field(init=False, repr=False, default_factory=Mutex)
    _auth: SchlageAuth | None
    device_id: str
    name: str
    model_name: str
    battery_level: int
    is_locked: bool
    is_jammed: bool
    firmware_version: str

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_mu"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._mu = Mutex()

    @classmethod
    def from_json(cls, auth, json):
        """Creates a Device from a JSON object."""
        return cls(
            _auth=auth,
            device_id=json["deviceId"],
            name=json["name"],
            model_name=json["modelName"],
            battery_level=json["attributes"]["batteryLevel"],
            is_locked=json["attributes"]["lockState"] == 1,
            is_jammed=json["attributes"]["lockState"] == 2,
            firmware_version=json["attributes"]["mainFirmwareVersion"],
        )

    def _update_with(self, json):
        new_obj = Device.from_json(self._auth, json)
        with self._mu:
            for field in dataclasses.fields(new_obj):
                setattr(self, field.name, getattr(new_obj, field.name))

    def update(self):
        """Updates the current device state."""
        self._update_with(self._auth.request("get", self.device_id).json())

    def _toggle(self, lock_state):
        self._update_with(
            self._auth.request(
                "put", self.device_id, json={"attributes": {"lockState": lock_state}}
            ).json()
        )

    def lock(self):
        """Locks the device."""
        self._toggle(1)

    def unlock(self):
        """Unlocks the device."""
        self._toggle(0)


class SchlageAPI:
    """API for interacting with the Schlage WiFi cloud service."""

    def __init__(self, auth: SchlageAuth) -> None:
        """Initializer."""
        self._auth = auth

    def devices(self) -> list[Device]:
        """Retreives all devies associated with this account."""
        response = self._auth.request("get", "")
        return [Device.from_json(self._auth, d) for d in response.json()]
