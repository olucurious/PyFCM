class FCMError(Exception):
    """
    PyFCM Error
    """
    pass

class AuthenticationError(FCMError):
    """
    API key not found or there was an error authenticating the sender
    """
    pass


class FCMServerError(FCMError):
    """
    Internal server error or timeout error on Firebase cloud messaging server
    """
    pass


class InvalidDataError(FCMError):
    """
    Invalid input
    """
    pass


class InternalPackageError(FCMError):
    """
    JSON parsing error, please create a new github issue describing what you're doing
    """
    pass
