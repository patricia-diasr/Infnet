from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class ComentarioBase(SQLModel):
    evento_id: int = Field(foreign_key = "evento.id")
    texto: str


class Comentario(ComentarioBase, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    autor_username: str = Field(foreign_key = "usuario.username")
    criado_em: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))


class ComentarioCreate(SQLModel):
    model_config = {"extra": "forbid"}
    texto: str = Field(min_length = 1, max_length = 1000)
