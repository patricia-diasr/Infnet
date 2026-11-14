import os
import sys
from importlib.metadata import version
from dotenv import load_dotenv
from openai import AsyncOpenAI

NOME_VARIAVEL = "OPENAI_API_KEY"

load_dotenv()

if not os.getenv(NOME_VARIAVEL):
    sys.exit(
        f"ERRO: a variável {NOME_VARIAVEL} não está definida. "
        "Copie .env.example para .env e preencha a chave."
    )

chave_lida_pelo_cliente = bool(AsyncOpenAI().api_key)

print(f"Pacote openai-agents instalado: versão {version('openai-agents')}")
print(f"Variável {NOME_VARIAVEL} definida: sim")
print(f"Cliente da OpenAI leu a chave do ambiente: {chave_lida_pelo_cliente}")
