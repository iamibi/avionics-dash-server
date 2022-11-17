# Third-Party Library
from flask_httpauth import HTTPTokenAuth
import jwt

# Custom Library
from avionics_dash_server.common import exceptions as ex
from avionics_dash_server.util.util import Util
from avionics_dash_server.config.settings import settings

# Create a Bearer token
bearer_token_auth = HTTPTokenAuth(scheme="Bearer")


def generate_token_for_username(username: str) -> str:
    try:
        current_utc_time = Util.utc_now()

        return jwt.encode(
            {
                "exp": Util.add_time_diff(timestamp=current_utc_time, hours=24),
                "iat": current_utc_time,
                "sub": str(Util.generate_uuid()),
                "username": username,
            },
            key=settings.credentials.jwt.key,
            algorithm="HS256",
        )
    except jwt.PyJWTError:
        raise ex.AuthenticationError(response_message="Unable to generate token!")


@bearer_token_auth.verify_token
def verify_token(token: str) -> bool:
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=settings.credentials.jwt.key,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub"], "verify_signature": True},
        )
    except jwt.ExpiredSignatureError:
        raise ex.AuthenticationError(response_code=401, response_message="Session Expired. Re-authentication Required!")
    except jwt.InvalidTokenError as invalid_jwt:
        raise ex.AuthenticationError(response_code=400, response_message=f"Bad Request. {invalid_jwt}")

    # TODO: Update this verification
    if decoded_token["username"] == "test":
        return True
    return False
