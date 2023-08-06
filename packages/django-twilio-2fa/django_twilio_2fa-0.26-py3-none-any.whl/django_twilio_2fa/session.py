from datetime import datetime
from django.utils import timezone
from .app_settings import conf


class TwoFASession(object):
    # Fields and their defaults
    _fields = {
        "verification_sid": {
            "type": "str",
            "default": None
        },
        "verification_method": {
            "type": "str",
            "default": None
        },
        "start_timestamp": {
            "type": "datetime",
            "default": None
        },
        "last_send_timestamp": {
            "type": "datetime",
            "default": None
        },
        "last_check_timestamp": {
            "type": "datetime",
            "default": None
        },
        "attempts": {
            "type": "int",
            "default": 0
        },
        "sends": {
            "type": "int",
            "default": 0
        },
        "success_redirect_url": {
            "type": "str",
            "default": None
        },
        "send_to_value": {
            "type": "str",
            "default": None
        },
        "send_to_display": {
            "type": "str",
            "default": None
        },
    }

    date_format = "%Y%m%dT%H:%M:%S"

    def __init__(self, request=None):
        self.request = request

        self.data = {}

        # Load up values from session, if request is available
        self.load()

    def load(self):
        """
        Loads the data dict with values from the session, if available
        """
        if not self.request:
            return

        for key, value in self.request.session.get(conf.session_data_key(), {}).items():
            if key not in self._fields:
                # Skip rogue session values
                continue

            field_data = self._fields[key]

            if field_data["type"] == "datetime":
                value = datetime.strptime(value, self.date_format)
                value = timezone.make_aware(value)

            self[key] = value

    def dump(self):
        """
        Dumps the data dict to the session, if available
        """
        if self.request:
            self.request.session[conf.session_data_key()] = self._to_dict()

        return self.data

    def _to_dict(self):
        payload = {}

        for key, data in self._fields.items():
            if key not in self.data:
                continue

            value = self.data[key]

            if data["type"] == "datetime":
                value = value.strftime(self.date_format)

            payload[key] = value

        return payload

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key, value):
        if key not in self._fields:
            raise KeyError(f"'{key}' is not a valid session field")

        field_data = self._fields[key]

        if field_data["type"] == "int":
            value = int(value)
        elif field_data["type"] == "datetime" and not isinstance(value, datetime):
            raise ValueError(f"'{key}' must be a datetime, not {type(value)}")

        self.data[key] = value

        self.dump()

    def get(self, key, default=None):
        if key not in self._fields:
            raise KeyError(f"'{key}' is not a valid session field")

        if default is None:
            default = self._fields[key].get("default")

        return self.data.get(key, default)

    def has(self, key, is_set=False):
        if key not in self._fields:
            return False

        return key in self.data or is_set is False

    def clear(self, exclude=None):
        if not exclude:
            exclude = []

        data = {}

        for key, value in self.data.items():
            if key not in exclude:
                continue

            data[key] = value

        self.data = data
        self.dump()
