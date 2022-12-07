# Standard Library
from typing import Dict, Optional

# Third-Party Library
import pymongo
from bson import ObjectId

# Custom Library
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings
from avionics_dash_server.common.constants import PasswordVerificationResult
from avionics_dash_server.models.user_model import User, PasswordModel
from avionics_dash_server.util.password_hasher import PasswordHasher

# Local Modules
from .database_service import DatabaseService


class UserService(DatabaseService):
    def __init__(self) -> None:
        super(UserService, self).__init__()
        self._collection = self._db[settings.db.avionics_dash.collections.users]
        self.index(mapping=[("email", pymongo.ASCENDING)], unique=True)

    def by_id(self, user_id: ObjectId, with_pass: bool = False) -> Optional[User]:
        user = self.find_one_by_id(bson_id=user_id)
        return self.__convert_to_user_obj(user=user, with_pass=with_pass)

    def by_email(self, email_id: str, with_pass: bool = False) -> Optional[User]:
        user = self.find_one(filter_dict={"email": email_id})
        return self.__convert_to_user_obj(user=user, with_pass=with_pass)

    def create_user(self, user_obj: Dict) -> None:
        password_hash = self.create_password_hash(password=user_obj["password"])
        user_obj["password"] = password_hash.dict()

        current_time = Util.utc_now()
        user_obj["created_at"] = user_obj["updated_at"] = current_time

        self.insert_one(doc=user_obj)

    def add_course_to_user(self, user_id: ObjectId, course_id: ObjectId) -> None:
        query = {"_id": user_id}
        update_hash = {"$push": {"course_ids": course_id}}
        self.update_one(query=query, update_hash=update_hash)

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

        return True if verification_status == PasswordVerificationResult.SUCCESS else False

    @classmethod
    def __convert_to_user_obj(cls, user: Optional[Dict], with_pass: bool = False) -> User:
        user_obj = None
        if user is not None:
            if with_pass is False:
                del user["password"]
            user["identifier"] = user["_id"]
            del user["_id"]
            user_obj = User.parse_obj(user)
        return user_obj
