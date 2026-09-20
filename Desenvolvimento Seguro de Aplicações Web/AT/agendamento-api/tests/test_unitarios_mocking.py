from datetime import timedelta
from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from app.security import auth
from app.security.ownership import requer_dono_ou_papel


class TestGetCurrentUserComMocking:

    def test_rejeita_token_com_tipo_client(self):
        payload_falso = {"sub": "laboratorio-parceiro", "tipo": "client", "scopes": ["horarios:leitura"]}

        with patch("app.security.auth.jwt.decode", return_value = payload_falso):
            with pytest.raises(HTTPException) as exc_info:
                auth.get_current_user(token = "token-qualquer", session = MagicMock())

        assert exc_info.value.status_code == 401


    def test_rejeita_token_sem_usuario_correspondente_no_banco(self):
        payload_falso = {"sub": "usuario-que-nao-existe-mais", "tipo": "usuario"}
        session_mock = MagicMock()

        with patch("app.security.auth.jwt.decode", return_value = payload_falso), patch("app.database.users_db.obter_usuario", return_value = None):
            with pytest.raises(HTTPException) as exc_info:
                auth.get_current_user(token = "token-qualquer", session = session_mock)

        assert exc_info.value.status_code == 401


    def test_aceita_token_valido_e_retorna_usuario_mockado(self):
        payload_falso = {"sub": "dra.pereira", "tipo": "usuario"}
        usuario_falso = MagicMock(username = "dra.pereira", role = "profissional")

        with patch("app.security.auth.jwt.decode", return_value = payload_falso), patch("app.database.users_db.obter_usuario", return_value = usuario_falso):
            resultado = auth.get_current_user(token = "token-qualquer", session = MagicMock())

        assert resultado.username == "dra.pereira"


class TestAutenticarUsuarioComMocking:

    def test_retorna_none_quando_usuario_nao_existe(self):
        with patch("app.database.users_db.obter_usuario", return_value = None):
            resultado = auth.autenticar_usuario(session = MagicMock(), username = "fantasma", password = "qualquer")

        assert resultado is None


    def test_retorna_none_quando_senha_esta_incorreta(self):
        usuario_falso = MagicMock(hashed_password="$2b$12$hashfalsoparaoteste")

        with patch("app.database.users_db.obter_usuario", return_value = usuario_falso), patch("app.security.auth.verificar_senha", return_value = False):
            resultado = auth.autenticar_usuario(session = MagicMock(), username = "dra.pereira", password = "senha-errada")

        assert resultado is None


    def test_retorna_usuario_quando_credenciais_corretas(self):
        usuario_falso = MagicMock(hashed_password="$2b$12$hashfalsoparaoteste")

        with patch("app.database.users_db.obter_usuario", return_value = usuario_falso), patch("app.security.auth.verificar_senha", return_value = True):
            resultado = auth.autenticar_usuario(session = MagicMock(), username = "dra.pereira", password = "senha456")

        assert resultado is usuario_falso


class TestRequerDonoOuPapelComMocking:

    def test_bloqueia_quando_nao_e_dono_nem_tem_papel_total(self):
        recurso_falso = MagicMock(profissional_username = "dra.pereira")
        buscar_falso = MagicMock(return_value = recurso_falso)
        usuario_falso = MagicMock(username = "dr.lima", role = "profissional")

        dependencia = requer_dono_ou_papel(
            buscar_falso, 
            campo_dono = "profissional_username",
            papeis_com_acesso_total = ["administrador"],
            descricao = "desta consulta", 
            nome_recurso = "consulta",
        )

        with pytest.raises(HTTPException) as exc_info:
            dependencia(id = 1, current_user = usuario_falso, session = MagicMock())

        assert exc_info.value.status_code == 403


    def test_permite_quando_e_o_dono(self):
        recurso_falso = MagicMock(profissional_username = "dra.pereira")
        buscar_falso = MagicMock(return_value = recurso_falso)
        usuario_falso = MagicMock(username = "dra.pereira", role = "profissional")

        dependencia = requer_dono_ou_papel(
            buscar_falso, 
            campo_dono = "profissional_username",
            papeis_com_acesso_total = ["administrador"],
            descricao = "desta consulta", 
            nome_recurso = "consulta",
        )

        resultado = dependencia(id = 1, current_user = usuario_falso, session = MagicMock())
        assert resultado is recurso_falso


    def test_permite_quando_papel_tem_acesso_total_mesmo_sem_ser_dono(self):
        recurso_falso = MagicMock(profissional_username = "dra.pereira")
        buscar_falso = MagicMock(return_value = recurso_falso)
        usuario_falso = MagicMock(username = "admin", role = "administrador")

        dependencia = requer_dono_ou_papel(
            buscar_falso, 
            campo_dono = "profissional_username",
            papeis_com_acesso_total = ["administrador"],
            descricao = "desta consulta", 
            nome_recurso = "consulta",
        )

        resultado = dependencia(id = 1, current_user = usuario_falso, session = MagicMock())
        assert resultado is recurso_falso


    def test_404_quando_recurso_nao_existe(self):
        buscar_falso = MagicMock(return_value = None)
        usuario_falso = MagicMock(username = "dra.pereira", role = "profissional")

        dependencia = requer_dono_ou_papel(
            buscar_falso, 
            campo_dono = "profissional_username",
            papeis_com_acesso_total = ["administrador"],
            descricao = "desta consulta", 
            nome_recurso = "consulta",
        )

        with pytest.raises(HTTPException) as exc_info:
            dependencia(id = 999, current_user = usuario_falso, session = MagicMock())

        assert exc_info.value.status_code == 404
