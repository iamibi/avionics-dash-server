# Third-Party Library
from bson import ObjectId

# Custom Library
from avionics_dash_server.common import constants as cst
from avionics_dash_server.util.util import Util
from avionics_dash_server.util.password_hasher import PasswordHasher
from avionics_dash_server.models.password_model import PasswordModel


class UserService:
    def create_password_hash(self, password: str) -> PasswordModel:
        password_hash = PasswordHasher.hash_password(password=password)
        timestamp_utc_now = Util.utc_now()

        return PasswordModel(password_hash=password_hash, created_at=timestamp_utc_now, updated_at=timestamp_utc_now)

    def verify_user_password(self, bson_id: ObjectId, provided_password: str) -> bool:
        # Extract the password from the database
        retrieved_hash = ""

        verification_status = PasswordHasher.verify_hashed_password(
            hashed_password=retrieved_hash, provided_password=provided_password
        )

        return True if verification_status.SUCCESS else False
