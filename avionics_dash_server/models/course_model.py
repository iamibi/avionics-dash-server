# Standard Library
from typing import Any, Dict, List
from datetime import datetime

# Third-Party Library
from bson import ObjectId
from pydantic import BaseModel, validator


class Module(BaseModel):
    identifier: ObjectId
    name: str
    desc: str
    url: str
    updated_at: datetime
    created_at: datetime

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
        serialized = self.dict()

        # Remove unnecessary fields
        del serialized["updated_at"]
        del serialized["created_at"]

        # Convert the bson id to string
        serialized["identifier"] = str(serialized["identifier"])

        return serialized


class Course(BaseModel):
    identifier: ObjectId
    img: str
    title: str
    price: str
    desc: str
    modules: List[ObjectId]
    assignments: List[ObjectId]
    updated_at: datetime
    created_at: datetime

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
        serialized = self.dict()

        # Remove unnecessary fields
        del serialized["updated_at"]
        del serialized["created_at"]

        # Convert the bson id to string
        serialized["identifier"] = str(serialized["identifier"])

        return serialized
