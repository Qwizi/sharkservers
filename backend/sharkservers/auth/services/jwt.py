"""
JWT Service.

This module contains JWTService class which is responsible for encoding and decoding JWT tokens.
"""

from datetime import datetime, timedelta

from jose import JWTError, jwt
from zoneinfo import ZoneInfo

from sharkservers.auth.exceptions import invalid_credentials_exception
from sharkservers.auth.schemas import TokenDataSchema
from sharkservers.auth.utils import now_datetime


class JWTService:
    """
    Service class for encoding and decoding JSON Web Tokens (JWT).

    Attributes
    ----------
        secret_key (str): The secret key used to encode and decode the JWT.
        algorithm (str): The algorithm used to encode and decode the JWT.
        expires_delta (timedelta): The expiration delta for the JWT.

    Methods
    -------
        encode: Encodes the given data into a JWT.
        decode: Decodes the given JWT.
        decode_token: Decodes the given JWT and returns the token data schema.
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS512",
        expires_delta: timedelta = timedelta(minutes=15),
    ) -> None:
        """Initialize the JWTService."""
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def encode(self, data: dict) -> (str, datetime):
        """
        Encodes the given data into a JWT.

        Args:
        ----
            data (dict): The data to be encoded.

        Returns:
        -------
            tuple: A tuple containing the encoded JWT and the expiration datetime.
        """  # noqa: D401
        to_encode = data.copy()
        expire = now_datetime() + self.expires_delta
        expire_with_timezone = expire.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
        to_encode.update({"exp": expire_with_timezone})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, expire

    def decode(self, token: str) -> dict:
        """
        Decodes the given JWT.

        Args:
        ----
            token (str): The JWT to be decoded.

        Returns:
        -------
            dict: The decoded JWT payload.
        """  # noqa: D401
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def decode_token(self, token: str) -> TokenDataSchema:
        """
        Decodes the given JWT and returns the token data schema.

        Args:
        ----
            token (str): The JWT to be decoded.

        Returns:
        -------
            TokenDataSchema: The decoded token data schema.

        Raises:
        ------
            invalid_credentials_exception: If the JWT is invalid or missing required data.
        """  # noqa: D401
        try:
            payload = self.decode(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise invalid_credentials_exception
            token_scopes = payload.get("scopes", [])
            secret = payload.get("secret")
            session_id = payload.get("session_id")

            return TokenDataSchema(
                user_id=user_id,
                scopes=token_scopes,
                secret=secret,
                session_id=session_id,
            )
        except JWTError as err:
            raise invalid_credentials_exception from err
