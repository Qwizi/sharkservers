from pydantic import BaseModel


class CreateAdmin(BaseModel):
    admin_username: str
    admin_password: str
    admin_email: str

