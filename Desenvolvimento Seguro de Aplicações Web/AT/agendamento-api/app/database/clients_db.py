from typing import List, Optional
from sqlmodel import Session
from app.models.cliente_api import ClienteAPI
from app.security.hashing import gerar_hash_senha, verificar_senha


def registrar_client(session: Session, client_id: str, client_secret: str, scopes: List[str]) -> ClienteAPI:
    cliente = ClienteAPI(client_id = client_id, hashed_secret = gerar_hash_senha(client_secret), scopes_csv = ",".join(scopes))
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def obter_client(session: Session, client_id: str) -> Optional[ClienteAPI]:
    return session.get(ClienteAPI, client_id)


def autenticar_client(session: Session, client_id: str, client_secret: str) -> Optional[ClienteAPI]:
    cliente = obter_client(session, client_id)

    if cliente is None:
        return None

    if not verificar_senha(client_secret, cliente.hashed_secret):
        return None

    return cliente
