from typing import Dict, Optional
from app.models.usuario import UsuarioCreate, UsuarioInDB
from app.security.hashing import gerar_hash_senha


_usuarios_db: Dict[str, UsuarioInDB] = {}


def criar_usuario(dados: UsuarioCreate) -> UsuarioInDB:
    usuario = UsuarioInDB(
        username=dados.username,
        email=dados.email,
        hashed_password=gerar_hash_senha(dados.password),
        role=dados.role
    )
    _usuarios_db[usuario.username] = usuario
    
    return usuario


def obter_usuario(username: str) -> Optional[UsuarioInDB]:
    return _usuarios_db.get(username)


def listar_usuarios() -> list[UsuarioInDB]:
    return list(_usuarios_db.values())
