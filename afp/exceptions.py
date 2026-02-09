class AFPException(Exception):
    pass


# API-specific exceptions


class ConfigurationError(AFPException):
    pass


class ClearingSystemError(AFPException):
    pass


class IPFSError(AFPException):
    pass


class ExchangeError(AFPException):
    pass


class DeviceError(AFPException):
    pass


# Exchange error sub-types


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
