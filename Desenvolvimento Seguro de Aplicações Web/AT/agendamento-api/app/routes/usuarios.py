from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import users_db
from app.database.session import get_session
from app.models.usuario import UsuarioCreate, UsuarioPublic
from app.security.auth import requer_papel


router = APIRouter(prefix = "/usuarios", tags = ["usuarios"])


@router.post("/", response_model = UsuarioPublic, status_code = status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCreate, session: Session = Depends(get_session)):
    if users_db.obter_usuario(session, dados.username) is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Username já cadastrado")

    return users_db.criar_usuario(session, dados)


@router.get("/", response_model = list[UsuarioPublic])
def listar_usuarios(session: Session = Depends(get_session), _admin=Depends(requer_papel(["administrador"]))):
    return users_db.listar_usuarios(session)
