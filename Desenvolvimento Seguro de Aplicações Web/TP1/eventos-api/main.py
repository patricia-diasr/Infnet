from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routes import eventos
from app.database import db


app = FastAPI(title="eventos-api", version="0.1.0")
app.include_router(eventos.router)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def status_servico():
    return {"status": "ok", "service": "eventos-api", "version": app.version}


@app.get("/eventos-html")
def pagina_eventos(request: Request):
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
