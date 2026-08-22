from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import db
from app.models.evento import EventoCreate, EventoInterno, EventoPublic, EventoUpdate
from app.models.usuario import UsuarioInDB
from app.security.auth import get_current_user, requer_escopo


router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.get("/", response_model=List[EventoPublic])
def listar_eventos(_=Depends(requer_escopo("eventos:leitura"))):
    return db.listar_eventos()


@router.post("/", response_model=EventoPublic, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, current_user: UsuarioInDB = Depends(get_current_user)):
    return db.criar_evento(evento, dono_username=current_user.username)


@router.get("/{evento_id}", response_model=EventoPublic)
def obter_evento(evento_id: int, _=Depends(requer_escopo("eventos:leitura"))):
    evento = db.obter_evento(evento_id)

    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    
    return evento


def obter_evento_e_verificar_dono(evento_id: int, current_user: UsuarioInDB = Depends(get_current_user)) -> EventoInterno:
    """Dependency injection: busca o evento e garante que o usuário autenticado é o organizador dono dele antes de permitir a edição."""
    
    evento = db.obter_evento(evento_id)
    
    if evento is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    
    if evento.dono_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não é o organizador responsável por este evento",
        )
    
    return evento


@router.put("/{evento_id}", response_model=EventoPublic)
def editar_evento(dados: EventoUpdate, evento: EventoInterno = Depends(obter_evento_e_verificar_dono)):
    return db.atualizar_evento(evento.id, dados)
