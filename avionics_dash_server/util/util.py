# Standard Library
import uuid
from typing import Any
from datetime import datetime, timezone, timedelta

# Third-Party Library
from bson import ObjectId
from email_validator import EmailNotValidError, validate_email

# Custom Library
from avionics_dash_server.common import exceptions as exc


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

    @classmethod
    def check_email(cls, email_id: str) -> str:
        try:
            validation = validate_email(email=email_id)
        except EmailNotValidError:
            raise exc.ValidationError("Invalid E-Mail passed!")

        return validation.email

    @classmethod
    def is_bson_id(cls, identifier: Any) -> bool:
        return ObjectId.is_valid(oid=identifier)

    @classmethod
    def is_email_id(cls, identifier: Any) -> bool:
        try:
            cls.check_email(email_id=identifier)
        except exc.ValidationError:
            return False
        return True
