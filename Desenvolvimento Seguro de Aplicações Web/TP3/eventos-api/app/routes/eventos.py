from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session
from app.database import db, search_index, comentarios_db
from app.database.session import get_session
from app.models.evento import Evento, EventoCreate, EventoPublic, EventoUpdate
from app.models.comentario import ComentarioCreate
from app.models.usuario import Usuario
from app.rate_limit import limiter
from app.security.auth import get_current_user, requer_escopo
from app.security.ownership import requer_dono


router = APIRouter(prefix = "/eventos", tags = ["eventos"])
verificar_dono_evento = requer_dono(db.obter_evento, campo_dono = "dono_username", descricao = "deste evento", nome_recurso = "evento")


@router.post("/{id}/comentarios", status_code = status.HTTP_201_CREATED)
def adicionar_comentario(id: int, dados: ComentarioCreate, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    evento = db.obter_evento(session, id)

    if evento is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Evento não encontrado")

    return comentarios_db.criar_comentario(session, id, current_user.username, dados.texto)


@router.get("/busca")
def buscar_eventos(nome: str, session: Session = Depends(get_session)):
    if not search_index.PADRAO_BUSCA_VALIDO.match(nome):
        raise HTTPException(status_code = 422, detail = "Termo de busca contém caracteres não permitidos")
    return search_index.buscar_por_nome(session, nome)


@router.get("/", response_model = List[EventoPublic])
@limiter.limit("100/minute")
def listar_eventos(request: Request, session: Session = Depends(get_session), _=Depends(requer_escopo("eventos:leitura"))):
    return db.listar_eventos(session)


@router.post("/", response_model = EventoPublic, status_code = status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    return db.criar_evento(session, evento, dono_username = current_user.username)


@router.get("/{id}", response_model = EventoPublic)
def obter_evento(id: int, session: Session = Depends(get_session), _=Depends(requer_escopo("eventos:leitura"))):
    evento = db.obter_evento(session, id)

    if evento is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Evento não encontrado")

    return evento


@router.put("/{id}", response_model = EventoPublic)
def editar_evento(dados: EventoUpdate, evento: Evento = Depends(verificar_dono_evento), session: Session = Depends(get_session)):
    return db.atualizar_evento(session, evento, dados)
