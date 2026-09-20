from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def obter_token_usuario(username: str, password: str) -> str:
    return client.post("/token", data = {"username": username, "password": password}).json()["access_token"]


def obter_token_laboratorio() -> str:
    resposta = client.post(
        "/token/client",
        data = {"grant_type": "client_credentials", "client_id": "laboratorio-parceiro", "client_secret": "segredo-laboratorio-123"},
    )

    return resposta.json()["access_token"]


def test_laboratorio_consulta_horarios_sem_ver_dados_de_paciente():
    token_prof = obter_token_usuario("dra.pereira", "senha456")
    client.post(
        "/consultas/",
        json = {"paciente_nome": "Paciente Sigiloso", "profissional_nome": "Dra. Carla Pereira", "especialidade": "Cardiologia", "data": "2026-11-10", "hora": "09:00:00"},
        headers = {"Authorization": f"Bearer {token_prof}"},
    )

    token_lab = obter_token_laboratorio()
    resposta = client.get(
        "/consultas/horarios-disponiveis",
        params = {"profissional_username": "dra.pereira", "data": "2026-11-10"},
        headers = {"Authorization": f"Bearer {token_lab}"},
    )

    assert resposta.status_code == 200
    corpo_como_texto = str(resposta.json())

    assert "Paciente Sigiloso" not in corpo_como_texto
    assert "09:00" not in resposta.json()["horarios_disponiveis"]


def test_laboratorio_nao_acessa_lista_completa_de_consultas():
    token_lab = obter_token_laboratorio()
    resposta = client.get("/consultas/", headers = {"Authorization": f"Bearer {token_lab}"})
    assert resposta.status_code == 401


def test_login_m2m_com_credenciais_invalidas_e_rejeitado():
    resposta = client.post(
        "/token/client",
        data = {"grant_type": "client_credentials", "client_id": "laboratorio-parceiro", "client_secret": "senha-errada"},
    )
    assert resposta.status_code == 401
