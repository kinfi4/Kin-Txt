from kin_txt_core.exceptions import AccessForbidden, KinNewsCoreException


class ReportAccessForbidden(AccessForbidden):
    pass


class ImpossibleToModifyProcessingReport(KinNewsCoreException):
    pass


class ReportNotFound(KinNewsCoreException):
    pass


class ReportDataNotFound(KinNewsCoreException):
    pass


class GenerationTemplateNotFound(KinNewsCoreException):
    pass


class BaseAuthError(KinNewsCoreException):
    pass


class UsernameAlreadyTakenError(BaseAuthError):
    pass


class LoginFailedError(BaseAuthError):
    pass
