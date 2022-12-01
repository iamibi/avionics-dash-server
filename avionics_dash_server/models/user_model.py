# Standard Library
from datetime import datetime
from typing import List

# Third-Party Library
from pydantic import BaseModel, validator

# Custom Library
from course_model import Course
from avionics_dash_server.common import UserRole

class PasswordModel(BaseModel):
    password_hash: str
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True, always=True)
    def check_timestamp(cls, v):
        # Check the timezone is UTC or not
        if v.tzname() != "UTC":
            raise ValueError("The timezone is not in UTC format")
        return v

class User:
    fname: str
    lname: str
    email: str
    password: PasswordModel
    role: UserRole

    def serialize(self):
        pass

    def fromDict(self):
        pass
