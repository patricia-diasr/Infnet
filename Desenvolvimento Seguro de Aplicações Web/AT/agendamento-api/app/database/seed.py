from sqlmodel import Session
from app.database import clients_db, users_db
from app.database.session import engine
from app.models.usuario import UsuarioCreate


def seed_dados_iniciais() -> None:
    with Session(engine) as session:

        if users_db.obter_usuario(session, "recepcao1") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "recepcao1", email = "recepcao1@clinica.com", password = "senha123", role = "recepcionista"))

        if users_db.obter_usuario(session, "dra.pereira") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "dra.pereira", email = "dra.pereira@clinica.com", password = "senha456", role = "profissional"))

        if users_db.obter_usuario(session, "dr.lima") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "dr.lima", email = "dr.lima@clinica.com", password = "senha789", role = "profissional"))

        if users_db.obter_usuario(session, "admin") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "admin", email = "admin@clinica.com", password = "admin123", role = "administrador"))

        if clients_db.obter_client(session, "laboratorio-parceiro") is None:
            clients_db.registrar_client(session, client_id = "laboratorio-parceiro", client_secret = "segredo-laboratorio-123", scopes = ["horarios:leitura"])
