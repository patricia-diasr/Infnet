from datetime import date, datetime
from pydantic import BaseModel


class EventoCreate(BaseModel):
    nome: str
    data: date
    organizador_nome: str
    organizador_email: str
    capacidade: int


class EventoPublic(BaseModel):
    id: int
    nome: str
    data: date
    organizador_nome: str
    organizador_email: str
    capacidade: int
    model_config = {"from_attributes": True}


class EventoInterno(EventoPublic):
    organizador_id: int
    audit_token: str
    criado_em: datetime
