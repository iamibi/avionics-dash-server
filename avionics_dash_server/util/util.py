# Standard Library
from datetime import datetime, timezone, timedelta
import uuid


class Util:
    @classmethod
    def utc_now(cls) -> datetime:
        return datetime.now(tz=timezone.utc)

    @classmethod
    def add_time_diff(
        cls, timestamp: datetime, days: float = None, hours: float = None, minutes: float = None, seconds: float = None
    ) -> datetime:
        if days is not None:
            time_diff = timedelta(days=days)
        elif hours is not None:
            time_diff = timedelta(hours=hours)
        elif minutes is not None:
            time_diff = timedelta(minutes=minutes)
        elif seconds is not None:
            time_diff = timedelta(seconds=seconds)
        else:
            raise ValueError("No valid value provided!")

        return timestamp + time_diff

    @classmethod
    def generate_uuid(cls) -> uuid.UUID:
        return uuid.uuid4()
