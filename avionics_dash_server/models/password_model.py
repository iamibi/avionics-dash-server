# Standard Library
from datetime import datetime

# Third-Party Library
from pydantic import BaseModel, validator


class PasswordModel(BaseModel):
    password_hash: str
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True, always=True)
    def check_timestamp(cls, v):
        # Check the timezone is UTC or not
        if v.tzname() != "UTC":
            return ValueError("The timezone is not in UTC format")
        return v
