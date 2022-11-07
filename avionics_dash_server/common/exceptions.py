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
