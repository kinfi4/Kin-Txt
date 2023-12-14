from pydantic import BaseModel


class User(BaseModel):
    username: str
    internal_user: bool = False
