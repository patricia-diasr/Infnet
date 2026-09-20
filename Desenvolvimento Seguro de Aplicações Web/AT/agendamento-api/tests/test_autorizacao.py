from datetime import timedelta
from fastapi.testclient import TestClient
from app.config import settings
from app.security import auth
from main import app
from jose import jwt


client = TestClient(app)


def obter_token(username: str, password: str) -> str:
    return client.post("/token", data = {"username": username, "password": password}).json()["access_token"]


def test_recepcionista_nao_pode_criar_consulta():
    token = obter_token("recepcao1", "senha123")
    resposta = client.post(
        "/consultas/",
        json = {"paciente_nome": "X", "profissional_nome": "Y", "especialidade": "Z", "data": "2026-12-01", "hora": "09:00:00"},
        headers = {"Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_recepcionista_nao_pode_editar_consulta():
    token_prof = obter_token("dra.pereira", "senha456")
    criada = client.post(
        "/consultas/",
        json = {"paciente_nome": "Paciente X", "profissional_nome": "Dra. Pereira", "especialidade": "Cardiologia", "data": "2026-12-02", "hora": "09:00:00"},
        headers = {"Authorization": f"Bearer {token_prof}"},
    ).json()

    token_recepcao = obter_token("recepcao1", "senha123")
    resposta = client.put(
        f"/consultas/{criada['id']}",
        json = {"especialidade": "Alterado", "data": "2026-12-02", "hora": "10:00:00", "status": "confirmada"},
        headers = {"Authorization": f"Bearer {token_recepcao}"},
    )

    assert resposta.status_code == 403


def test_token_expirado_e_rejeitado():
    claims = {"sub": "dra.pereira", "tipo": "usuario", "role": "profissional", "scopes": ["consultas:leitura", "consultas:escrita"]}
    token_expirado = auth.criar_jwt(claims, timedelta(minutes = -1))
    resposta = client.get("/consultas/", headers = {"Authorization": f"Bearer {token_expirado}"})
    assert resposta.status_code == 401


def test_laboratorio_nao_escala_escopo_alem_do_contratado():
    resposta = client.post(
        "/token/client",
        data = {
            "grant_type": "client_credentials",
            "client_id": "laboratorio-parceiro",
            "client_secret": "segredo-laboratorio-123",
            "scope": "horarios:leitura consultas:leitura consultas:escrita usuarios:leitura",
        },
    )

    assert resposta.status_code == 200
    payload = jwt.decode(resposta.json()["access_token"], settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
    assert payload["scopes"] == ["horarios:leitura"]
