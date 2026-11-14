from datetime import datetime
from pathlib import Path
from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

INSTRUCOES = """Você é o assistente de política de cancelamento da NeoStream, uma plataforma de streaming por assinatura.
Seu papel é responder, em português e de forma clara e cordial, perguntas gerais sobre o cancelamento de assinaturas.

Política de cancelamento de referência:
- O cancelamento pode ser feito a qualquer momento, pelo aplicativo ou pelo site, em Conta > Assinatura > Cancelar assinatura.
- Não há multa nem fidelidade.
- O acesso continua até o fim do período já pago.
- Não há reembolso proporcional do período em andamento. Cobranças indevidas ou duplicadas são analisadas pelo suporte.
- A assinatura pode ser reativada a qualquer momento.
- As regras valem para os planos básico, padrão e premium.

Responda apenas com base nessa política. Se a pergunta fugir do tema ou pedir uma informação que a política não traz, diga que não tem essa informação e indique o suporte da NeoStream."""

PERGUNTAS = [
    "Como faço para cancelar minha assinatura?",
    "Se eu cancelar hoje, até quando posso assistir e receberei reembolso?",
    "Quanto custa o plano premium?",
]

agente = Agent(name = "Assistente de política de cancelamento", instructions = INSTRUCOES)

linhas = [
    "# Respostas do primeiro agente",
    "",
    f"Execução registrada em {datetime.now():%d/%m/%Y às %H:%M}.",
    "",
    "## Instruções do agente",
    "",
    *(f"> {linha}" for linha in INSTRUCOES.splitlines()),
    "",
]

for numero, pergunta in enumerate(PERGUNTAS, start = 1):
    resultado = Runner.run_sync(agente, pergunta)
    print(f"Pergunta {numero}: {pergunta}\n{resultado.final_output}\n")
    linhas += [
        f"## Pergunta {numero}",
        "",
        f"**Pergunta:** {pergunta}",
        "",
        "**Resposta do agente:**",
        "",
        *(f"> {linha}" for linha in resultado.final_output.splitlines()),
        "",
    ]

Path("respostas_primeiro_agente.md").write_text("\n".join(linhas), encoding = "utf-8")
