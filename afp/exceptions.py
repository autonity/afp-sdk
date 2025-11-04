class AFPException(Exception):
    pass


class ConfigurationError(AFPException):
    pass


class ClearingSystemError(AFPException):
    pass


class ExchangeError(AFPException):
    pass


class AuthenticationError(ExchangeError):
    pass


class AuthorizationError(ExchangeError):
    pass


class NotFoundError(ExchangeError):
    pass


class RateLimitExceeded(ExchangeError):
    pass


class ValidationError(ExchangeError):
    pass
