import secrets
from datetime import datetime, timezone
from itertools import count
from typing import Dict, List, Optional
from app.models.evento import EventoCreate, EventoInterno, EventoUpdate


_eventos_db: Dict[int, EventoInterno] = {}
_id_seq = count(1)
_organizador_id_seq = count(1000)


def criar_evento(dados: EventoCreate, dono_username: str) -> EventoInterno:
    novo_id = next(_id_seq)
    evento = EventoInterno(
        id=novo_id,
        nome=dados.nome,
        data=dados.data,
        organizador_nome=dados.organizador_nome,
        organizador_email=dados.organizador_email,
        capacidade=dados.capacidade,
        dono_username=dono_username,
        organizador_id=next(_organizador_id_seq),
        audit_token=secrets.token_hex(16),
        criado_em=datetime.now(timezone.utc),
    )

    _eventos_db[novo_id] = evento
    return evento


def listar_eventos() -> List[EventoInterno]:
    return list(_eventos_db.values())


def obter_evento(evento_id: int) -> Optional[EventoInterno]:
    return _eventos_db.get(evento_id)


def atualizar_evento(evento_id: int, dados: EventoUpdate) -> EventoInterno:
    evento = _eventos_db[evento_id]
    atualizado = evento.model_copy(update={
        "nome": dados.nome,
        "data": dados.data,
        "capacidade": dados.capacidade,
    })

    _eventos_db[evento_id] = atualizado
    return atualizado
