from pydantic import field_validator, model_validator, ConfigDict, BaseModel, Field


class User(BaseModel):
    username: str
    internal_user: bool = False


class UserLoginEntity(BaseModel):
    username: str
    password: str = ""


class UserRegistrationEntity(BaseModel):
    username: str
    password: str
    password_repeated: str = Field(..., alias="passwordRepeated")

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def validate_passwords_equal(self) -> "UserRegistrationEntity":
        if self.password is None or self.password_repeated is None or self.password != self.password_repeated:
            raise ValueError("Passwords must be equal!")

        return self

    @field_validator('*', mode="before")
    def empty_str_to_none(cls, value: str) -> str | None:
        if value == "":
            return None

        return value
