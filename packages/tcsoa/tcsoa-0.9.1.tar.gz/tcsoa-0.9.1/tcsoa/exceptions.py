import enum


class Severity(enum.Enum):
    information = 1
    warning = 2
    error = 3
    user_error = 4


class TcError(Exception):
    def __init__(self, message: str, code: int, level: Severity):
        super(TcError, self).__init__(f"[{level.name}] Code {code} - {message}")
        self.message = message
        self.code = code
        self.level = level


class ServiceException(TcError):
    pass


class InvalidCredentialsException(TcError):
    pass


class InternalServerException(TcError):
    pass
