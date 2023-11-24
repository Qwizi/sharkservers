from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

from jose import jwt, JWTError

from src.auth.exceptions import invalid_credentials_exception
from src.auth.schemas import TokenDataSchema
from src.auth.utils import now_datetime


class JWTService:
    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS512",
            expires_delta: timedelta = timedelta(minutes=15),
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def encode(self, data: dict) -> (str, datetime):
        to_encode = data.copy()
        expire = now_datetime() + self.expires_delta
        expire_with_timezone = expire.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
        to_encode.update({"exp": expire_with_timezone})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, expire

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def decode_token(self, token: str) -> TokenDataSchema:
        try:
            payload = self.decode(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise invalid_credentials_exception
            token_scopes = payload.get("scopes", [])
            secret = payload.get("secret")
            session_id = payload.get("session_id")

            return TokenDataSchema(
                user_id=int(user_id), scopes=token_scopes, secret=secret, session_id=session_id
            )
        except JWTError as e:
            raise invalid_credentials_exception
