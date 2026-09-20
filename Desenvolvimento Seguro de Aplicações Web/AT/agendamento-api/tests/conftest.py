import pytest
from app.database.seed import seed_dados_iniciais
from app.database.session import criar_tabelas
from app.rate_limit import limiter


@pytest.fixture(scope = "session", autouse = True)
def preparar_banco_de_dados():
    criar_tabelas()
    seed_dados_iniciais()


@pytest.fixture(autouse = True)
def resetar_rate_limiter():
    limiter.reset()
    yield
