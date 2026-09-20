from typing import List
from sqlmodel import Session, select
from app.models.comentario import Comentario


def criar_comentario(session: Session, evento_id: int, autor_username: str, texto: str) -> Comentario:
    comentario = Comentario(evento_id = evento_id, autor_username = autor_username, texto = texto)
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return comentario


def listar_comentarios_do_evento(session: Session, evento_id: int) -> List[Comentario]:
    return list(session.exec(select(Comentario).where(Comentario.evento_id == evento_id)).all())
