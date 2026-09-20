from typing import List, Optional
from sqlmodel import Session, select
from app.models.usuario import Usuario, UsuarioCreate
from app.security.hashing import gerar_hash_senha


def criar_usuario(session: Session, dados: UsuarioCreate) -> Usuario:
    usuario = Usuario(username = dados.username, email = dados.email, role = dados.role, hashed_password = gerar_hash_senha(dados.password))
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def obter_usuario(session: Session, username: str) -> Optional[Usuario]:
    return session.get(Usuario, username)


def listar_usuarios(session: Session) -> List[Usuario]:
    return list(session.exec(select(Usuario)).all())
