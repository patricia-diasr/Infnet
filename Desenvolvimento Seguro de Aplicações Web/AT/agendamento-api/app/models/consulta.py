from datetime import date, datetime, time, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class ConsultaBase(SQLModel):
    paciente_nome: str
    profissional_nome: str
    especialidade: str
    data: date
    hora: time


class Consulta(ConsultaBase, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    status: str = "agendada"
    profissional_username: str = Field(foreign_key = "usuario.username")
    criado_por_ip: str
    audit_token: str
    criado_em: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))


class ConsultaCreate(SQLModel):
    model_config = {"extra": "forbid"}
    paciente_nome: str = Field(min_length = 1, max_length = 200)
    profissional_nome: str = Field(min_length = 1, max_length = 200)
    especialidade: str = Field(min_length = 1, max_length = 100)
    data: date
    hora: time


class ConsultaUpdate(SQLModel):
    model_config = {"extra": "forbid"}
    especialidade: str = Field(min_length = 1, max_length = 100)
    data: date
    hora: time
    status: str = "agendada"


class ConsultaPublic(ConsultaBase):
    id: int
    status: str
    profissional_username: str
