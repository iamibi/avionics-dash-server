class AvionicsDashError(Exception):
    """Base error for all the AvionicsDash functionality"""

    message: str = None

    def __init__(self, message: str = "") -> None:
        self.message = message
        super(AvionicsDashError, self).__init__(message)


class ConfigurationError(AvionicsDashError):
    pass


class DatabaseError(AvionicsDashError):
    pass


class DbCollectionNotSet(DatabaseError):
    MESSAGE = "The collection is not set!"

    def __init__(self, message: str = None):
        if message is None:
            self.message = self.MESSAGE
        super(DbCollectionNotSet, self).__init__(message)


class AuthenticationError(AvionicsDashError):
    response_code: int = None
    response_message: str = ""

    def __init__(self, response_code: int = None, response_message: str = None) -> None:
        if response_code is not None:
            self.response_code = response_code
        if response_message is not None:
            self.response_message = response_message
        super(AuthenticationError, self).__init__(self.response_message)


class ServiceInitializationError(AvionicsDashError):
    pass


class ValidationError(AvionicsDashError):
    pass


class UserAlreadyExistsError(ValidationError):
    def __init__(self):
        super(UserAlreadyExistsError, self).__init__("User Already Exists!")
