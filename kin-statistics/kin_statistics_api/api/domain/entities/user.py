from pydantic import BaseModel


class CreateUserEntity(BaseModel):
    username: str
