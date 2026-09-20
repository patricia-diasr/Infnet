import logging
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def obter_token(username: str, password: str) -> str:
    resposta = client.post("/token", data = {"username": username, "password": password})
    return resposta.json()["access_token"]


def test_usuario_sem_papel_administrador_e_impedido_de_rota_restrita():
    token_profissional = obter_token("dra.pereira", "senha456")
    resposta = client.get("/usuarios/", headers = {"Authorization": f"Bearer {token_profissional}"})
    assert resposta.status_code == 403


def test_login_administrador_exige_mfa_e_nao_retorna_codigo_na_resposta():
    resposta = client.post("/token", data = {"username": "admin", "password": "admin123"})
    assert resposta.status_code == 200

    corpo = resposta.json()
    assert corpo["mfa_required"] is True
    assert "codigo_simulado" not in corpo


def test_admin_acessa_rota_restrita_apos_completar_mfa(caplog):
    with caplog.at_level(logging.WARNING, logger = "mfa"):
        etapa1 = client.post("/token", data = {"username": "admin", "password": "admin123"}).json()

    codigo = None

    for registro in caplog.records:
        if "[MFA] Código para admin:" in registro.message:
            codigo = registro.message.split(":")[1].strip().split(" ")[0]

    assert codigo is not None, "código MFA não encontrado no log (canal separado)"

    etapa2 = client.post("/token/mfa", json = {"mfa_token": etapa1["mfa_token"], "codigo": codigo})
    assert etapa2.status_code == 200

    token_admin = etapa2.json()["access_token"]
    resposta = client.get("/usuarios/", headers = {"Authorization": f"Bearer {token_admin}"})
    assert resposta.status_code == 200
