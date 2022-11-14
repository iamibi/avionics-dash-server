# Standard Library
from datetime import datetime, timezone


class Util:
    @classmethod
    def utc_now(cls):
        return datetime.now(tz=timezone.utc)
