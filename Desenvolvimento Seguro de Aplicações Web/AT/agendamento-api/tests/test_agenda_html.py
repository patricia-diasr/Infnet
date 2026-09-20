from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_agenda_html_sem_credenciais_e_rejeitada():
    resposta = client.get("/agenda-html")
    assert resposta.status_code == 401


def test_agenda_html_com_credenciais_validas_funciona():
    resposta = client.get("/agenda-html", auth = ("recepcao1", "senha123"))
    assert resposta.status_code == 200


def test_agenda_html_com_senha_incorreta_e_rejeitada():
    resposta = client.get("/agenda-html", auth = ("recepcao1", "senha-errada"))
    assert resposta.status_code == 401
