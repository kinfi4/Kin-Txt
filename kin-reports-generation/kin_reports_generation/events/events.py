from kin_news_core.messaging import BasicEvent


class ModelDeleted(BasicEvent):
    code: str
    username: str
