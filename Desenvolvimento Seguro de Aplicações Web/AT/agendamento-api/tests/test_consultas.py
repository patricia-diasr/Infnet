from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def obter_token(username: str, password: str) -> str:
    resposta = client.post("/token", data = {"username": username, "password": password})
    return resposta.json()["access_token"]


def cabecalho_profissional() -> dict:
    token = obter_token("dra.pereira", "senha456")
    return {"Authorization": f"Bearer {token}"}


def test_criar_consulta_com_sucesso():
    payload = {
        "paciente_nome": "Lucas Oliveira",
        "profissional_nome": "Dra. Carla Pereira",
        "especialidade": "Cardiologia",
        "data": "2026-10-05",
        "hora": "14:30:00",
    }

    resposta = client.post("/consultas/", json = payload, headers = cabecalho_profissional())
    assert resposta.status_code == 201
    corpo = resposta.json()

    assert corpo["paciente_nome"] == "Lucas Oliveira"
    assert corpo["profissional_nome"] == "Dra. Carla Pereira"
    assert corpo["status"] == "agendada"    
    assert "id" in corpo


def test_criar_consulta_sem_autenticacao_e_rejeitada():
    payload = {
        "paciente_nome": "Lucas Oliveira",
        "profissional_nome": "Dra. Carla Pereira",
        "especialidade": "Cardiologia",
        "data": "2026-10-05",
        "hora": "14:30:00",
    }

    resposta = client.post("/consultas/", json = payload)
    assert resposta.status_code == 401


def test_listar_consultas_inclui_consulta_criada():
    payload = {
        "paciente_nome": "Bruna Sales",
        "profissional_nome": "Dra. Carla Pereira",
        "especialidade": "Cardiologia",
        "data": "2026-11-01",
        "hora": "09:00:00",
    }

    criada = client.post("/consultas/", json = payload, headers = cabecalho_profissional()).json()
    resposta = client.get("/consultas/", headers = cabecalho_profissional())

    assert resposta.status_code == 200
    ids = [c["id"] for c in resposta.json()]
    assert criada["id"] in ids


def test_criar_consulta_nao_expoe_campos_internos():
    payload = {
        "paciente_nome": "Carlos Mendes",
        "profissional_nome": "Dra. Carla Pereira",
        "especialidade": "Cardiologia",
        "data": "2026-10-06",
        "hora": "11:00:00",
    }

    resposta = client.post("/consultas/", json = payload, headers = cabecalho_profissional())
    corpo = resposta.json()

    assert "criado_por_ip" not in corpo
    assert "audit_token" not in corpo
    assert "criado_em" not in corpo


def test_obter_consulta_inexistente_retorna_404():
    resposta = client.get("/consultas/99999", headers = cabecalho_profissional())
    assert resposta.status_code == 404


def test_profissional_nao_ve_consulta_de_paciente_de_outro_profissional():
    token_dra_pereira = obter_token("dra.pereira", "senha456")
    criada = client.post(
        "/consultas/",
        json = {"paciente_nome": "Paciente da Dra. Pereira", "profissional_nome": "Dra. Pereira", "especialidade": "Cardiologia", "data": "2026-10-07", "hora": "10:00:00"},
        headers = {"Authorization": f"Bearer {token_dra_pereira}"},
    ).json()

    token_dr_lima = obter_token("dr.lima", "senha789")
    resposta = client.get(f"/consultas/{criada['id']}", headers = {"Authorization": f"Bearer {token_dr_lima}"})

    assert resposta.status_code == 403


def test_profissional_nao_edita_consulta_de_paciente_de_outro_profissional():
    token_dra_pereira = obter_token("dra.pereira", "senha456")
    criada = client.post(
        "/consultas/",
        json = {"paciente_nome": "Paciente Protegido", "profissional_nome": "Dra. Pereira", "especialidade": "Cardiologia", "data": "2026-10-08", "hora": "10:00:00"},
        headers = {"Authorization": f"Bearer {token_dra_pereira}"},
    ).json()

    token_dr_lima = obter_token("dr.lima", "senha789")
    resposta = client.put(
        f"/consultas/{criada['id']}",
        json = {"especialidade": "Hackeado", "data": "2026-01-01", "hora": "00:00:00", "status": "cancelada"},
        headers = {"Authorization": f"Bearer {token_dr_lima}"},
    )

    assert resposta.status_code == 403


def test_profissional_nao_cancela_consulta_de_paciente_de_outro_profissional():
    token_dra_pereira = obter_token("dra.pereira", "senha456")
    criada = client.post(
        "/consultas/",
        json = {"paciente_nome": "Outro Paciente Protegido", "profissional_nome": "Dra. Pereira", "especialidade": "Cardiologia", "data": "2026-10-09", "hora": "10:00:00"},
        headers = {"Authorization": f"Bearer {token_dra_pereira}"},
    ).json()

    token_dr_lima = obter_token("dr.lima", "senha789")
    resposta = client.delete(f"/consultas/{criada['id']}", headers = {"Authorization": f"Bearer {token_dr_lima}"})

    assert resposta.status_code == 403


def test_criar_consulta_com_campo_extra_e_rejeitada():
    payload = {
        "paciente_nome": "Diego Alves", 
        "profissional_nome": "Dra. Pereira",
        "especialidade": "Cardiologia", 
        "data": "2026-10-10", 
        "hora": "09:00:00",
        "campo_nao_documentado": "valor_suspeito",
    }
    resposta = client.post("/consultas/", json = payload, headers = cabecalho_profissional())
    assert resposta.status_code == 422
