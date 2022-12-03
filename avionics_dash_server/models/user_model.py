# Standard Library
from typing import Any, Dict
from datetime import date, datetime

# Third-Party Library
from bson import ObjectId
from pydantic import BaseModel, validator

# Custom Library
from avionics_dash_server.common.constants import Roles


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
    dob: date
    gender: str
    email: str
    role: Roles.UserRole
    address: str
    phone_number: str
    password: PasswordModel = None
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True

    @validator("identifier", pre=True, always=True)
    def check_identifier(cls, v):
        if ObjectId.is_valid(oid=v) is False:
            raise ValueError("Invalid BSON Object ID Passed")
        return v

    @validator("created_at", "updated_at", pre=True, always=True)
    def check_timestamp(cls, v):
        if isinstance(v, datetime) is False:
            raise TypeError("Invalid datetime type passed!")

        # Check the timezone is UTC or not
        if v.tzname() != "UTC":
            raise ValueError("The timezone is not in UTC format")
        return v

    def api_serialize(self) -> Dict[str, Any]:
        return {
            "id": str(self.identifier),
            "firstName": self.first_name,
            "lastName": self.last_name,
            "dob": self.dob.isoformat(),
            "gender": self.gender,
            "email": self.email,
            "role": self.role.value,
            "address": self.address,
            "phoneNumber": self.phone_number,
        }
