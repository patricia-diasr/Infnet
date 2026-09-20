from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database import inscricoes_db
from app.database.session import get_session
from app.models.inscricao import Inscricao, InscricaoCreate, InscricaoPublic
from app.models.usuario import Usuario
from app.security.auth import get_current_user
from app.security.ownership import requer_dono


router = APIRouter(prefix = "/inscricoes", tags = ["inscricoes"])
verificar_dono_inscricao = requer_dono(inscricoes_db.obter_inscricao, campo_dono = "participante_username", descricao = "desta inscrição", nome_recurso = "inscrição")


@router.post("/", response_model = InscricaoPublic, status_code = status.HTTP_201_CREATED)
def criar_inscricao(dados: InscricaoCreate, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    return inscricoes_db.criar_inscricao(session, dados.evento_id, current_user.username)


@router.get("/{id}", response_model = InscricaoPublic)
def obter_inscricao(inscricao: Inscricao = Depends(verificar_dono_inscricao)):
    return inscricao
