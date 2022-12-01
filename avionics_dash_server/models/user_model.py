# Standard Library
from datetime import datetime

# Third-Party Library
from pydantic import BaseModel, validator
from bson import ObjectId


class PasswordModel(BaseModel):
    password_hash: str
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True, always=True)
    def check_timestamp(cls, v):
        if isinstance(v, datetime) is False:
            raise TypeError("Invalid datetime type passed!")

        # Check the timezone is UTC or not
        if v.tzname() != "UTC":
            raise ValueError("The timezone is not in UTC format")
        return v


class User(BaseModel):
    identifier: ObjectId = None
    first_name: str
    last_name: str
    email: str
    password: PasswordModel
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
