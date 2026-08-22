from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.database import clients_db
from app.security import auth


router = APIRouter(tags=["autenticacao"])


class MfaConfirmacao(BaseModel):
    mfa_token: str
    codigo: str


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = auth.autenticar_usuario(form_data.username, form_data.password)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if usuario.role == "administrador":
        return {"mfa_required": True, **auth.iniciar_mfa(usuario)}

    token = auth.criar_token_acesso_usuario(usuario)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token/mfa")
def confirmar_mfa(dados: MfaConfirmacao):
    usuario = auth.confirmar_mfa(dados.mfa_token, dados.codigo)

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código MFA inválido ou expirado")

    token = auth.criar_token_acesso_usuario(usuario)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token/client")
def login_client(grant_type: str = Form(...), client_id: str = Form(...), client_secret: str = Form(...), scope: str = Form("")):
    if grant_type != "client_credentials":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="grant_type deve ser 'client_credentials'")

    cliente = clients_db.autenticar_client(client_id, client_secret)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="client_id ou client_secret inválidos")

    escopos_solicitados = scope.split() if scope else cliente["scopes"]
    escopos_concedidos = [s for s in escopos_solicitados if s in cliente["scopes"]]

    token = auth.criar_jwt(
        {"sub": client_id, "tipo": "client", "scopes": escopos_concedidos},
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token, "token_type": "bearer"}
