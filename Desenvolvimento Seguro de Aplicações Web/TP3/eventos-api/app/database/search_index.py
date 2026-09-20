import re
from sqlalchemy import text
from sqlmodel import Session


PADRAO_BUSCA_VALIDO = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9 ]{1,100}$")


def buscar_por_nome(session: Session, termo: str) -> list[dict]:
    query = text("SELECT id, nome FROM evento WHERE nome LIKE :termo")
    resultado = session.exec(query, params={"termo": f"%{termo}%"}).all()
    return [{"id": row[0], "nome": row[1]} for row in resultado]
