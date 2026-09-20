from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlmodel import Session
from app.database import comentarios_db, db
from app.database.seed import seed_dados_iniciais
from app.database.session import criar_tabelas, get_session
from app.routes import auth, eventos, inscricoes, usuarios
from app.rate_limit import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    seed_dados_iniciais()
    yield


app = FastAPI(title = "eventos-api", version = "0.3.0", lifespan = lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ORIGENS_PERMITIDAS = [
    "http://localhost:3000",
    "https://app.eventos-empresa.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGENS_PERMITIDAS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.middleware("http")
async def adicionar_cabecalhos_seguranca(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(eventos.router)
app.include_router(inscricoes.router)
templates = Jinja2Templates(directory = "templates")


@app.get("/")
def status_servico():
    return {"status": "ok", "service": "eventos-api", "version": app.version}


@app.get("/eventos-html/{id}", response_class = HTMLResponse)
def pagina_detalhe_evento(id: int, request: Request, session: Session = Depends(get_session)):
    evento = db.obter_evento(session, id)

    if evento is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Evento não encontrado")

    comentarios = comentarios_db.listar_comentarios_do_evento(session, id)
    return templates.TemplateResponse(request = request, name = "evento_detail.html", context = {"evento": evento, "comentarios": comentarios})
