from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class InscricaoBase(SQLModel):
    evento_id: int = Field(foreign_key = "evento.id")


class Inscricao(InscricaoBase, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    participante_username: str = Field(foreign_key = "usuario.username")
    criado_em: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))


class InscricaoCreate(SQLModel):
    model_config = {"extra": "forbid"}
    evento_id: int


class InscricaoPublic(InscricaoBase):
    id: int
    participante_username: str
    criado_em: datetime
