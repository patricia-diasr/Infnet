from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UsuarioBase(SQLModel):
    username: str
    email: str
    role: str = "profissional"


class Usuario(UsuarioBase, table = True):
    username: str = Field(primary_key = True)
    hashed_password: str


class UsuarioCreate(SQLModel):
    model_config = {"extra": "forbid"}
    username: str
    email: EmailStr
    password: str = Field(min_length = 8, max_length = 72)
    role: str = "profissional"


class UsuarioPublic(UsuarioBase):
    pass
