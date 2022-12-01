# Standard Library
from typing import Dict, Union

# Third-Party Library
import pymongo
from bson import ObjectId

# Custom Library
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings
from avionics_dash_server.util.password_hasher import PasswordHasher
from avionics_dash_server.models.password_model import PasswordModel

# Local Modules
from .database_service import DatabaseService


class UserService(DatabaseService):
    def __init__(self) -> None:
        super(UserService, self).__init__()
        self._collection = self._db[settings.db.avionics_dash.collections.users]
        self.index(mapping=[("email", pymongo.ASCENDING)], unique=True)

    def by_id(self, bson_id: ObjectId, with_pass: bool = False) -> Union[Dict, None]:
        user = self.find_one(filter_dict={"_id": bson_id})
        if user is not None and with_pass is False:
            del user["password"]
        return user

    def by_email(self, email_id: str, with_pass: bool = False) -> Union[Dict, None]:
        user = self.find_one(filter_dict={"email": email_id})
        if user is not None and with_pass is False:
            del user["password"]
        return user

    def create_user(self, user_obj: Dict) -> None:
        password_hash = self.create_password_hash(password=user_obj["password"])
        user_obj["password"] = password_hash.dict()

        current_time = Util.utc_now()
        user_obj["created_at"] = user_obj["updated_at"] = current_time

        self.insert_one(doc=user_obj)

    @classmethod
    def create_password_hash(cls, password: str) -> PasswordModel:
        password_hash = PasswordHasher.hash_password(password=password)
        timestamp_utc_now = Util.utc_now()

        return PasswordModel(password_hash=password_hash, created_at=timestamp_utc_now, updated_at=timestamp_utc_now)

    @classmethod
    def verify_user_password(cls, retrieved_hash: str, provided_password: str) -> bool:
        verification_status = PasswordHasher.verify_hashed_password(
            hashed_password=retrieved_hash, provided_password=provided_password
        )

        return True if verification_status.SUCCESS else False
