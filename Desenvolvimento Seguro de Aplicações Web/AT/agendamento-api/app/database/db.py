import secrets
from datetime import date as date_type, datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select
from app.models.consulta import Consulta, ConsultaCreate, ConsultaUpdate


def criar_consulta(session: Session, dados: ConsultaCreate, criado_por_ip: str, profissional_username: str) -> Consulta:
    consulta = Consulta(
        **dados.model_dump(),
        status = "agendada",
        profissional_username = profissional_username,
        criado_por_ip = criado_por_ip,
        audit_token = secrets.token_hex(16),
        criado_em = datetime.now(timezone.utc),
    )
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


def listar_consultas(session: Session) -> List[Consulta]:
    return list(session.exec(select(Consulta)).all())


def obter_consulta(session: Session, consulta_id: int) -> Optional[Consulta]:
    return session.get(Consulta, consulta_id)


def listar_consultas_do_dia(session: Session, data: date_type) -> List[Consulta]:
    return list(session.exec(select(Consulta).where(Consulta.data == data)).all())


def atualizar_consulta(session: Session, consulta: Consulta, dados: ConsultaUpdate) -> Consulta:
    consulta.especialidade = dados.especialidade
    consulta.data = dados.data
    consulta.hora = dados.hora
    consulta.status = dados.status
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


def excluir_consulta(session: Session, consulta: Consulta) -> None:
    session.delete(consulta)
    session.commit()
