from typing import List, Optional
from sqlmodel import Session, select
from app.models.inscricao import Inscricao


def criar_inscricao(session: Session, evento_id: int, participante_username: str) -> Inscricao:
    inscricao = Inscricao(evento_id = evento_id, participante_username = participante_username)
    session.add(inscricao)
    session.commit()
    session.refresh(inscricao)
    return inscricao


def obter_inscricao(session: Session, inscricao_id: int) -> Optional[Inscricao]:
    return session.get(Inscricao, inscricao_id)


def listar_inscricoes(session: Session) -> List[Inscricao]:
    return list(session.exec(select(Inscricao)).all())
