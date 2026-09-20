from datetime import date as date_type
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session
from app.database import db
from app.database.session import get_session
from app.models.consulta import Consulta, ConsultaCreate, ConsultaPublic, ConsultaUpdate
from app.models.usuario import Usuario
from app.rate_limit import limiter
from app.security.auth import get_current_user, requer_escopo, requer_papel
from app.security.ownership import requer_dono_ou_papel


router = APIRouter(prefix = "/consultas", tags = ["consultas"])
HORARIOS_PADRAO = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]


verificar_acesso_leitura = requer_dono_ou_papel(
    db.obter_consulta, 
    campo_dono = "profissional_username",
    papeis_com_acesso_total = ["recepcionista", "administrador"],
    descricao = "desta consulta", 
    nome_recurso = "consulta",
)


verificar_acesso_escrita = requer_dono_ou_papel(
    db.obter_consulta, 
    campo_dono = "profissional_username",
    papeis_com_acesso_total = ["administrador"],
    descricao = "desta consulta", 
    nome_recurso = "consulta",
)


@router.get("/horarios-disponiveis")
def consultar_horarios_disponiveis(
    profissional_username: str,
    data: date_type,
    session: Session = Depends(get_session),
    _=Depends(requer_escopo("horarios:leitura")),
):
    ocupados = {
        c.hora.strftime("%H:%M")
        for c in db.listar_consultas(session)
        if c.profissional_username == profissional_username and c.data == data
    }
    disponiveis = [h for h in HORARIOS_PADRAO if h not in ocupados]
    return {"profissional_username": profissional_username, "data": data.isoformat(), "horarios_disponiveis": disponiveis}


@router.get("/", response_model = List[ConsultaPublic])
@limiter.limit("100/minute")
def listar_consultas(request: Request, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    todas = db.listar_consultas(session)

    if current_user.role == "profissional":
        return [c for c in todas if c.profissional_username == current_user.username]

    return todas


@router.post("/", response_model = ConsultaPublic, status_code = status.HTTP_201_CREATED)
def criar_consulta(
    consulta: ConsultaCreate,
    request: Request,
    current_user: Usuario = Depends(requer_papel(["profissional"])),
    session: Session = Depends(get_session),
):
    ip_cliente = request.client.host if request.client else "desconhecido"
    return db.criar_consulta(session, consulta, criado_por_ip = ip_cliente, profissional_username = current_user.username)


@router.get("/{id}", response_model = ConsultaPublic)
def obter_consulta(consulta: Consulta = Depends(verificar_acesso_leitura)):
    return consulta


@router.put("/{id}", response_model = ConsultaPublic)
def editar_consulta(dados: ConsultaUpdate, consulta: Consulta = Depends(verificar_acesso_escrita), session: Session = Depends(get_session)):
    return db.atualizar_consulta(session, consulta, dados)


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def cancelar_consulta(consulta: Consulta = Depends(verificar_acesso_escrita), session: Session = Depends(get_session)):
    db.excluir_consulta(session, consulta)
