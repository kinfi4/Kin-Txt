from kin_txt_core.messaging import BasicEvent


class ModelDeleted(BasicEvent):
    code: str
    username: str
