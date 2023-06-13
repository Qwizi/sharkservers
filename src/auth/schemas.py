from pydantic import BaseModel, validator, Field, EmailStr


class RegisterUserSchema(BaseModel):
    username: str = Field(
        max_length=32, min_length=4, regex="^[a-zA-Z0-9_]+$", default="your_username"
    )
    email: EmailStr = Field(default="test@test.pl")
    password: str = Field(max_length=255, default="test123456")
    password2: str = Field(max_length=255, default="test123456")

    @validator("password2")
    def passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    secret: str
    scopes: list[str] = []


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ActivateUserCodeSchema(BaseModel):
    code: str = Field(max_length=5)


class ResendActivationCodeSchema(BaseModel):
    email: EmailStr


class UserActivatedSchema(BaseModel):
    id: int
    is_activated: bool
