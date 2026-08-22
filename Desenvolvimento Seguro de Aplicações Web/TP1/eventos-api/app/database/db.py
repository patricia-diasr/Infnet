import secrets
from datetime import datetime
from itertools import count
from app.models.evento import EventoCreate, EventoInterno


_eventos_db: dict[int, EventoInterno] = {}
_id_seq = count(1)
_organizador_id_seq = count(1000)


def criar_evento(dados: EventoCreate) -> EventoInterno:
    novo_id = next(_id_seq)
    evento = EventoInterno(
        id=novo_id,
        nome=dados.nome,
        data=dados.data,
        organizador_nome=dados.organizador_nome,
        organizador_email=dados.organizador_email,
        capacidade=dados.capacidade,
        organizador_id=next(_organizador_id_seq),
        audit_token=secrets.token_hex(16),
        criado_em=datetime.utcnow(),
    )

    _eventos_db[novo_id] = evento
    return evento


def listar_eventos() -> list[EventoInterno]:
    return list(_eventos_db.values())


def obter_evento(evento_id: int) -> EventoInterno | None:
    return _eventos_db.get(evento_id)
