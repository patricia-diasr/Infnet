from contextlib import asynccontextmanager
from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlmodel import Session
from app.config import settings
from app.database import db, users_db
from app.database.seed import seed_dados_iniciais
from app.database.session import criar_tabelas, get_session
from app.models.usuario import Usuario
from app.rate_limit import limiter
from app.routes import auth, consultas, usuarios
from app.security.hashing import verificar_senha


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    seed_dados_iniciais()
    yield


app = FastAPI(title = "agendamento-api", version = "0.2.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.middleware("http")
async def adicionar_cabecalhos_seguranca(request: Request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"

    if request.url.path == "/docs":
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com;"
        )
    else:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'"
        )

    return response


app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(consultas.router)


templates = Jinja2Templates(directory = "templates")
security_basic = HTTPBasic()


def verificar_acesso_agenda(
    credentials: HTTPBasicCredentials = Depends(security_basic),
    session: Session = Depends(get_session),
) -> Usuario:
    usuario = users_db.obter_usuario(session, credentials.username)

    if usuario is None or not verificar_senha(credentials.password, usuario.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Credenciais inválidas", headers = {"WWW-Authenticate": "Basic"})

    return usuario


@app.exception_handler(Exception)
async def excecao_nao_tratada(request: Request, exc: Exception):
    return JSONResponse(status_code = 500, content = {"detail": "Erro interno do servidor."})


@app.get("/")
def status_servico():
    return {"status": "ok", "service": "agendamento-api", "version": app.version}


@app.get("/agenda-html", response_class = HTMLResponse)
def pagina_agenda_do_dia(
    request: Request,
    _usuario: Usuario = Depends(verificar_acesso_agenda),
    session: Session = Depends(get_session),
):
    hoje = date.today()
    consultas_hoje = db.listar_consultas_do_dia(session, hoje)
    return templates.TemplateResponse(
        request = request, 
        name = "agenda.html",
        context = {"consultas": consultas_hoje, "data_hoje": hoje},
    )
