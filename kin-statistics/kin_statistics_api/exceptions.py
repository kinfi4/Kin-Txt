from kin_news_core.exceptions import AccessForbidden, KinNewsCoreException


class ReportAccessForbidden(AccessForbidden):
    pass


class UsernameTaken(KinNewsCoreException):
    pass


class ImpossibleToModifyProcessingReport(KinNewsCoreException):
    pass


class ReportNotFound(KinNewsCoreException):
    pass


class ReportDataNotFound(KinNewsCoreException):
    pass
