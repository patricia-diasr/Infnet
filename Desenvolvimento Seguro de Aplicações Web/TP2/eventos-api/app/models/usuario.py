from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "organizador"


class UsuarioPublic(BaseModel):
    username: str
    email: EmailStr
    role: str
    model_config = {"from_attributes": True}


class UsuarioInDB(UsuarioPublic):
    hashed_password: str
