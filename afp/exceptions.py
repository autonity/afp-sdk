class BaseException(Exception):
    pass


class ClearingSystemError(BaseException):
    pass


class ExchangeError(BaseException):
    pass


class AuthenticationError(ExchangeError):
    pass


class AuthorizationError(ExchangeError):
    pass


class NotFoundError(ExchangeError):
    pass


class ValidationError(ExchangeError):
    pass
