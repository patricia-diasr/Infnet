from sqlmodel import Session
from app.database import clients_db, users_db
from app.database.session import engine
from app.models.usuario import UsuarioCreate


def seed_dados_iniciais() -> None:
    with Session(engine) as session:
        if users_db.obter_usuario(session, "maria") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "maria", email = "maria@empresa.com", password = "senha123", role = "organizador"))

        if users_db.obter_usuario(session, "joao") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "joao", email = "joao@empresa.com", password = "senha456", role = "organizador"))

        if users_db.obter_usuario(session, "admin") is None:
            users_db.criar_usuario(session, UsuarioCreate(username = "admin", email = "admin@empresa.com", password = "admin123", role = "administrador"))

        if clients_db.obter_client(session, "parceiro-integracao") is None:
            clients_db.registrar_client(session, client_id = "parceiro-integracao", client_secret = "segredo-super-secreto-123", scopes = ["eventos:leitura"])
