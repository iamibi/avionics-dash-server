# Standard Library
from enum import Enum


class App:
    BLUEPRINT = "avionics_dash_blueprint"
    APP_ENV = "APP_ENV"
    TEST_ENV = "test"
    DEV_ENV = "dev"
    PROD_ENV = "prod"
    VALID_ENVS = {TEST_ENV, DEV_ENV, PROD_ENV}

    class Env:
        DB_USERNAME = "DB_USERNAME"
        DB_PASSWORD = "DB_PASSWORD"
        JWT_KEY = "JWT_KEY"


class Credentials:
    USERNAME = "username"
    PASSWORD = "password"
    KEY = "key"
    DB = {USERNAME: "db_username", PASSWORD: "db_password"}
    JWT = {KEY: "jwt_key"}


class HttpMethod:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class AssignmentType(Enum):
    PERSONAL = 1
    GROUP = 2
    DISCUSSION = 3


class PasswordVerificationResult(Enum):
    SUCCESS = 1
    FAILED = 2


class Roles:
    class UserRole(str, Enum):
        VISITOR = "v"
        STUDENT = "s"
        INSTRUCTOR = "i"
        ADMIN = "a"

    VALID_USER_ROLES = {UserRole.VISITOR.value, UserRole.STUDENT.value, UserRole.INSTRUCTOR.value, UserRole.ADMIN.value}


class Limits:
    USER_NAME_LIMIT = 10
    PASSWORD_LENGTH_LIMIT = 25
    ADDRESS_LIMIT = 50
