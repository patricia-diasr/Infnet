from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import db
from app.routes import auth, eventos, usuarios


app = FastAPI(title="eventos-api", version="0.2.0")
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(eventos.router)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def status_servico():
    return {"status": "ok", "service": "eventos-api", "version": app.version}


@app.get("/eventos-html", response_class=HTMLResponse)
def pagina_lista_eventos(request: Request):
    return templates.TemplateResponse(
        request=request, name="eventos_list.html",
        context={"eventos": db.listar_eventos()},
    )


@app.get("/eventos-html/{evento_id}")
def pagina_detalhe_evento(request: Request, evento_id: int):
    evento = db.obter_evento(evento_id)
    return templates.TemplateResponse(
        request=request, name="evento_detail.html",
        context={"evento": evento},
    )
