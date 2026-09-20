import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from app.database import users_db
from app.database.session import get_session
from app.models.usuario import Usuario
from app.security.hashing import verificar_senha


SECRET_KEY = "chave-secreta-de-desenvolvimento"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

ESCOPOS_POR_PAPEL: Dict[str, List[str]] = {
    "participante": ["eventos:leitura"],
    "organizador": ["eventos:leitura", "eventos:escrita"],
    "administrador": ["eventos:leitura", "eventos:escrita", "usuarios:leitura"],
}

_mfa_pendentes: Dict[str, Dict[str, str]] = {}


def autenticar_usuario(session: Session, username: str, password: str) -> Optional[Usuario]:
    usuario = users_db.obter_usuario(session, username)

    if usuario is None:
        return None

    if not verificar_senha(password, usuario.hashed_password):
        return None

    return usuario


def criar_jwt(claims: dict, expira_em: timedelta) -> str:
    dados = claims.copy()
    dados["exp"] = datetime.now(timezone.utc) + expira_em
    return jwt.encode(dados, SECRET_KEY, algorithm = ALGORITHM)


def criar_token_acesso_usuario(usuario: Usuario) -> str:
    claims = {"sub": usuario.username, "tipo": "usuario", "role": usuario.role, "scopes": ESCOPOS_POR_PAPEL.get(usuario.role, [])}
    return criar_jwt(claims, timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))


def iniciar_mfa(usuario: Usuario) -> Dict[str, str]:
    codigo = f"{secrets.randbelow(1_000_000):06d}"
    mfa_token = secrets.token_hex(16)
    _mfa_pendentes[mfa_token] = {"username": usuario.username, "codigo": codigo}
    return {"mfa_token": mfa_token, "codigo_simulado": codigo}


def confirmar_mfa(session: Session, mfa_token: str, codigo: str) -> Optional[Usuario]:
    pendente = _mfa_pendentes.get(mfa_token)

    if pendente is None or pendente["codigo"] != codigo:
        return None

    del _mfa_pendentes[mfa_token]
    return users_db.obter_usuario(session, pendente["username"])


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Usuario:
    credenciais_invalidas = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token inválido ou expirado", headers = {"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

    except JWTError:
        raise credenciais_invalidas

    if payload.get("tipo") != "usuario":
        raise credenciais_invalidas

    username = payload.get("sub")
    usuario = users_db.obter_usuario(session, username) if username else None

    if usuario is None:
        raise credenciais_invalidas

    return usuario


def requer_papel(papeis_permitidos: List[str]):
    def verificador(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.role not in papeis_permitidos:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Papel '{usuario.role}' não tem permissão para esta operação")

        return usuario

    return verificador


def requer_escopo(escopo_necessario: str):
    def verificador(token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        except JWTError:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token inválido ou expirado", headers = {"WWW-Authenticate": "Bearer"})

        escopos = payload.get("scopes", [])

        if escopo_necessario not in escopos:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Escopo '{escopo_necessario}' não concedido a este token")

        return payload

    return verificador
