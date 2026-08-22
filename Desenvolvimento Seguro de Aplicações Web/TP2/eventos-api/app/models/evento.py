from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class EventoCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    data: date
    organizador_nome: str
    organizador_email: EmailStr
    capacidade: int = Field(..., gt=0)


class EventoUpdate(BaseModel):
    nome: str
    data: date
    capacidade: int = Field(..., gt=0)


class EventoPublic(BaseModel):
    id: int
    nome: str
    data: date
    organizador_nome: str
    organizador_email: EmailStr
    capacidade: int
    dono_username: str
    model_config = {"from_attributes": True}


class EventoInterno(EventoPublic):
    organizador_id: int
    audit_token: str
    criado_em: datetime
