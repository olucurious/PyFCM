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


class FCMNotRegisteredError(FCMError):
    """
    push token is not registered
    https://firebase.google.com/docs/reference/fcm/rest/v1/ErrorCode
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


class RetryAfterException(Exception):
    """
    Retry-After must be handled by external logic.
    """
    def __init__(self, delay):
        self.delay = delay
