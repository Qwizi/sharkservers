import datetime

from pydantic import BaseModel, validator, Field, EmailStr


class UsernameRegex(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=32,
        regex=r"^[a-zA-Z0-9_-]+$",
        strip_whitespace=True,
        default="username",
    )


class PasswordSchema(BaseModel):
    password: str = Field(min_length=8, max_length=255)
    password2: str = Field(min_length=8, max_length=255)

    @validator("password2")
    def passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")


class RegisterUserSchema(UsernameRegex, PasswordSchema):
    email: EmailStr


class TokenDetailsSchema(BaseModel):
    token: str
    token_type: str
    exp: datetime.datetime


class TokenSchema(BaseModel):
    access_token: TokenDetailsSchema
    refresh_token: TokenDetailsSchema


class TokenDataSchema(BaseModel):
    user_id: int | None = None
    secret: str
    scopes: list[str] = []
    session_id: str | None


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class ActivateUserCodeSchema(BaseModel):
    code: str = Field(max_length=5)


class ResendActivationCodeSchema(BaseModel):
    email: EmailStr


class UserActivatedSchema(BaseModel):
    id: int
    is_activated: bool


class EmailConfirmSchema(BaseModel):
    old_email: EmailStr
    new_email: EmailStr
    is_confirmed: bool


class ResetPasswordSchema(ActivateUserCodeSchema, PasswordSchema):
    pass


class SteamAuthSchema(BaseModel):
    openid_ns: str
    openid_mode: str
    openid_op_endpoint: str
    openid_claimed_id: str
    openid_identity: str
    openid_return_to: str
    openid_response_nonce: str
    openid_assoc_handle: str
    openid_signed: str
    openid_sig: str
