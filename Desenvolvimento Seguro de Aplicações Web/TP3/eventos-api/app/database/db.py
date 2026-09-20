import secrets
from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select
from app.models.evento import Evento, EventoCreate, EventoUpdate


def criar_evento(session: Session, dados: EventoCreate, dono_username: str) -> Evento:
    evento = Evento(
        **dados.model_dump(),
        dono_username = dono_username,
        organizador_id = secrets.randbelow(9000) + 1000,
        audit_token = secrets.token_hex(16),
        criado_em = datetime.now(timezone.utc),
    )
    session.add(evento)
    session.commit()
    session.refresh(evento)
    return evento


def listar_eventos(session: Session) -> List[Evento]:
    return list(session.exec(select(Evento)).all())


def obter_evento(session: Session, evento_id: int) -> Optional[Evento]:
    return session.get(Evento, evento_id)


def atualizar_evento(session: Session, evento: Evento, dados: EventoUpdate) -> Evento:
    evento.nome = dados.nome
    evento.data = dados.data
    evento.capacidade = dados.capacidade
    session.add(evento)
    session.commit()
    session.refresh(evento)
    return evento
