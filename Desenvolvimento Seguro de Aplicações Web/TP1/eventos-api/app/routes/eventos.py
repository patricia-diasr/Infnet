from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models.evento import EventoCreate, EventoPublic


router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.get("/", response_model=list[EventoPublic])
def listar_eventos():
    return db.listar_eventos()


@router.post("/", response_model=EventoPublic, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate):
    return db.criar_evento(evento)


@router.get("/{evento_id}", response_model=EventoPublic)
def obter_evento(evento_id: int):
    evento = db.obter_evento(evento_id)

    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    return evento


@router.post("/demo-sem-response-model", tags=["demonstracao"])
def criar_evento_sem_response_model(evento: EventoCreate):
    return db.criar_evento(evento)
