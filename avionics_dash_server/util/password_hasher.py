# Standard Library
import os
import hmac
import base64
import hashlib

# Custom Library
from avionics_dash_server.common.constants import PasswordVerificationResult


class PasswordHasher:
    __SALT_LENGTH = 32
    __SHA_256 = "sha256"
    __ENCODING_UTF_8 = "utf-8"
    __PBKDF2_ITERATIONS = 100_000

    # 32 bytes
    __SUBKEY_LENGTH = 256 // 8

    __EMPTY_VALUES = {None, ""}

    @classmethod
    def hash_password(cls, *, password: str) -> str:
        if password in cls.__EMPTY_VALUES:
            raise ValueError("Invalid value passed!")

        password_hash = base64.standard_b64encode(cls.__hash_password(password=password))
        return password_hash.decode(encoding=cls.__ENCODING_UTF_8)

    @classmethod
    def verify_hashed_password(cls, *, hashed_password: str, provided_password: str) -> PasswordVerificationResult:
        if hashed_password in cls.__EMPTY_VALUES:
            raise ValueError("Invalid hash passed!")
        if provided_password in cls.__EMPTY_VALUES:
            raise ValueError("Invalid value passed!")

        if cls.__verify_hashed_password(hashed_password=hashed_password, provided_password=provided_password) is True:
            return PasswordVerificationResult.SUCCESS
        return PasswordVerificationResult.FAILED

    @classmethod
    def __hash_password(cls, *, password: str) -> bytes:
        salt = cls.__create_salt()
        password_bytes = password.encode(cls.__ENCODING_UTF_8)
        password_hash = cls.__create_password_hash(password=password_bytes, salt=salt)

        return salt + password_hash

    @classmethod
    def __verify_hashed_password(cls, *, hashed_password: str, provided_password: str) -> bool:
        try:
            # Convert the `hashed_password` and `provided_password` from string to bytes
            hashed_password_bytes = base64.standard_b64decode(hashed_password)

            # Return false if the length of the decoded bytes is not salt length + subkey length
            if len(hashed_password_bytes) != cls.__SALT_LENGTH + cls.__SUBKEY_LENGTH:
                return False

            provided_password_bytes = provided_password.encode(cls.__ENCODING_UTF_8)

            # Extract the salt and password hash from the `hashed_password`
            stored_salt = hashed_password_bytes[0 : cls.__SALT_LENGTH]
            expected_subkey = hashed_password_bytes[cls.__SALT_LENGTH :]

            # Generate the hash for the `provided_password` using the stored password salt
            actual_subkey = cls.__create_password_hash(password=provided_password_bytes, salt=stored_salt)

            # Compare both the digests in a fixed time to prevent timing attacks
            return hmac.compare_digest(actual_subkey, expected_subkey)
        except Exception:
            return False

    @classmethod
    def __create_password_hash(cls, *, password: bytes, salt: bytes) -> bytes:
        # Generate PBKDF2-HMAC-SHA256 Hash
        return hashlib.pbkdf2_hmac(
            hash_name=cls.__SHA_256,
            password=password,
            salt=salt,
            iterations=cls.__PBKDF2_ITERATIONS,
            dklen=cls.__SUBKEY_LENGTH,
        )

    @classmethod
    def __create_salt(cls) -> bytes:
        return os.urandom(cls.__SALT_LENGTH)
