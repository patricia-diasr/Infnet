from fastapi import APIRouter, HTTPException, status
from app.database import users_db
from app.models.usuario import UsuarioCreate, UsuarioPublic


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCreate):
    if users_db.obter_usuario(dados.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já cadastrado")

    return users_db.criar_usuario(dados)
