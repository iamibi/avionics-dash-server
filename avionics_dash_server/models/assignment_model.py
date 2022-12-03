# Standard Library
from datetime import datetime

# Third-Party Library
from bson import ObjectId
from pydantic import BaseModel, validator


class Assignment(BaseModel):
    identifier: ObjectId
    name: str
    desc: str
    due: datetime
    points: int
    submitted: bool
    grade: str
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
