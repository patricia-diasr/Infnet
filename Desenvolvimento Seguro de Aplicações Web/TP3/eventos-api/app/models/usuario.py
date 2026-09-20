from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UsuarioBase(SQLModel):
    username: str
    email: str
    role: str = "organizador"


class Usuario(UsuarioBase, table = True):
    username: str = Field(primary_key = True)
    hashed_password: str


class UsuarioCreate(SQLModel):
    model_config = {"extra": "forbid"}
    username: str
    email: EmailStr
    password: str
    role: str = "organizador"


class UsuarioPublic(UsuarioBase):
    pass
