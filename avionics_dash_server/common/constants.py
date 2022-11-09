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


class Credentials:
    USERNAME = "username"
    PASSWORD = "password"
    DB = {USERNAME: "db_username", PASSWORD: "db_password"}


class HttpMethod:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
