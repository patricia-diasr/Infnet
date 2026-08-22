from typing import Dict, List, Optional
from app.security.hashing import gerar_hash_senha, verificar_senha


_clients_db: Dict[str, dict] = {}


def registrar_client(client_id: str, client_secret: str, scopes: List[str]) -> None:
    _clients_db[client_id] = {
        "client_id": client_id,
        "hashed_secret": gerar_hash_senha(client_secret),
        "scopes": scopes,
    }


def obter_client(client_id: str) -> Optional[dict]:
    return _clients_db.get(client_id)


def autenticar_client(client_id: str, client_secret: str) -> Optional[dict]:
    cliente = obter_client(client_id)

    if cliente is None:
        return None

    if not verificar_senha(client_secret, cliente["hashed_secret"]):
        return None

    return cliente


registrar_client(
    client_id="parceiro-integracao",
    client_secret="segredo-de-desenvolvimento",
    scopes=["eventos:leitura"]
)
