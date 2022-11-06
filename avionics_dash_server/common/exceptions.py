class AvionicsDashError(Exception):
    """Base error for all the AvionicsDash functionality"""

    message: str = None

    def __init__(self, message: str = "") -> None:
        self.message = message
        super(AvionicsDashError, self).__init__(message)


class ConfigurationError(AvionicsDashError):
    pass
