from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from app.config import settings
from app.database import clients_db
from app.database.session import get_session
from app.rate_limit import limiter
from app.security import auth


router = APIRouter(tags = ["autenticacao"])


class MfaConfirmacao(BaseModel):
    mfa_token: str
    codigo: str


@router.post("/token")
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    usuario = auth.autenticar_usuario(session, form_data.username, form_data.password)

    if usuario is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Usuário ou senha incorretos", headers = {"WWW-Authenticate": "Bearer"})

    if usuario.role == "administrador":
        mfa_token = auth.iniciar_mfa(usuario)
        return {"mfa_required": True, "mfa_token": mfa_token}

    token = auth.criar_token_acesso_usuario(usuario)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token/mfa")
def confirmar_mfa(dados: MfaConfirmacao, session: Session = Depends(get_session)):
    usuario = auth.confirmar_mfa(session, dados.mfa_token, dados.codigo)

    if usuario is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Código MFA inválido ou expirado")

    token = auth.criar_token_acesso_usuario(usuario)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token/client")
def login_client(
    grant_type: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    scope: str = Form(""),
    session: Session = Depends(get_session),
):
    if grant_type != "client_credentials":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "grant_type deve ser 'client_credentials'")

    cliente = clients_db.autenticar_client(session, client_id, client_secret)

    if cliente is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "client_id ou client_secret inválidos")

    escopos_permitidos = cliente.scopes()
    escopos_solicitados = scope.split() if scope else escopos_permitidos
    escopos_concedidos = [s for s in escopos_solicitados if s in escopos_permitidos]

    token = auth.criar_jwt({"sub": client_id, "tipo": "client", "scopes": escopos_concedidos}, timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
