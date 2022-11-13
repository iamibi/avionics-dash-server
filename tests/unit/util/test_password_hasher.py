# Standard Library
import base64

# Third-Party Library
import pytest

# Custom Library
from avionics_dash_server.common.constants import PasswordVerificationResult
from avionics_dash_server.util.password_hasher import PasswordHasher


class TestPasswordHasher:
    def test_hash_password_valid(self):
        password = "atestpassword"
        password_hash = PasswordHasher.hash_password(password=password)

        assert isinstance(password_hash, str) is True

    def test_verify_hashed_password_valid(self):
        password = "atestpassword"
        password_hash = PasswordHasher.hash_password(password=password)

        assert isinstance(password_hash, str) is True

        password_verification = PasswordHasher.verify_hashed_password(
            hashed_password=password_hash, provided_password=password
        )

        assert password_verification == PasswordVerificationResult.SUCCESS

        password_verification = PasswordHasher.verify_hashed_password(
            hashed_password=password_hash, provided_password="abcd1234"
        )

        assert password_verification == PasswordVerificationResult.FAILED

    def test_hash_password_invalid(self):
        for invalid_val in {None, ""}:
            with pytest.raises(expected_exception=ValueError) as v_err:
                PasswordHasher.hash_password(password=invalid_val)
            assert v_err.type == ValueError
            assert str(v_err.value) == "Invalid value passed!"

    def test_verify_hashed_password_invalid(self):
        for invalid_val in {None, ""}:
            with pytest.raises(expected_exception=ValueError) as v_err:
                PasswordHasher.verify_hashed_password(hashed_password="abcd1234", provided_password=invalid_val)
            assert v_err.type == ValueError
            assert str(v_err.value) == "Invalid value passed!"

            with pytest.raises(expected_exception=ValueError) as v_err:
                PasswordHasher.verify_hashed_password(hashed_password=invalid_val, provided_password="atestpassword")
            assert v_err.type == ValueError
            assert str(v_err.value) == "Invalid hash passed!"

        encoded_str = base64.standard_b64encode(b"abcd1234").decode("utf-8")
        assert (
            PasswordHasher.verify_hashed_password(hashed_password=encoded_str, provided_password="abcd1234")
            == PasswordVerificationResult.FAILED
        )
