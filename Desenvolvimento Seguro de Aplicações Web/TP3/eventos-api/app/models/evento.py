from datetime import date, datetime, timezone
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class EventoBase(SQLModel):
    nome: str
    data: date
    organizador_nome: str
    organizador_email: str
    capacidade: int


class Evento(EventoBase, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    dono_username: str = Field(foreign_key = "usuario.username")
    organizador_id: int
    audit_token: str
    criado_em: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))


class EventoCreate(SQLModel):
    model_config = {"extra": "forbid"}
    nome: str = Field(min_length = 1, max_length = 200)
    data: date
    organizador_nome: str
    organizador_email: EmailStr
    capacidade: int = Field(gt = 0)


class EventoUpdate(SQLModel):
    model_config = {"extra": "forbid"}
    nome: str
    data: date
    capacidade: int = Field(gt = 0)


class EventoPublic(EventoBase):
    id: int
    dono_username: str
