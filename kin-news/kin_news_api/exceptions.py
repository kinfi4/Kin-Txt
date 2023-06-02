class KinNewsBaseException(Exception):
    pass


class BaseAuthError(KinNewsBaseException):
    pass


class UsernameAlreadyTakenError(BaseAuthError):
    pass


class LoginFailedError(BaseAuthError):
    pass


class UserIsNotSubscribed(KinNewsBaseException):
    pass


class UserMaxSubscriptionsExceeded(KinNewsBaseException):
    pass


class ChannelDoesNotExists(KinNewsBaseException):
    pass


class InvalidURIParams(KinNewsBaseException):
    pass


class UserAlreadyFetchingNews(KinNewsBaseException):
    pass
