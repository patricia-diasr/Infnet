
from datetime import datetime
from pathlib import Path
from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class RespostaAgente(BaseModel):
    categoria_risco: str = Field(
        description = "Categoria de risco de churn: baixo, médio ou alto."
    )
    recomendacao: str = Field(
        description = "Ação recomendada ao time de retenção, em uma ou duas frases."
    )
    confianca: float = Field(
        description = "Confiança na análise, de 0 a 1, de acordo com a informação disponível."
    )

INSTRUCOES = """Você é um analista de risco de churn da NeoStream, uma plataforma de streaming por assinatura.

Dada uma pergunta do time de retenção sobre um assinante, avalie o risco de ele cancelar e recomende uma ação.

Fatores de risco no modelo de churn da NeoStream:
- menos tempo de assinatura aumenta o risco.
- menor uso médio semanal aumenta o risco.
- mais reclamações aumentam o risco.
- plano, método de pagamento e dispositivo têm pouca influência.

Se a pergunta trouxer a probabilidade de churn estimada pelo modelo, use esta regra para a categoria: baixo abaixo de 15%, médio entre 15% e 30%, alto acima de 30%.

Use somente as informações da pergunta e não invente dados. Se faltar informação importante, reduza a confiança e diga na recomendação o que falta."""

PERGUNTA = (
    "Um assinante do plano básico tem 2 meses de assinatura, usa em média 3 horas por semana e já fez 3 reclamações. Qual o risco de ele cancelar e o que devemos fazer?"
)

agente = Agent(
    name = "Analista de risco de churn",
    instructions = INSTRUCOES,
    output_type = RespostaAgente,
)

resposta = Runner.run_sync(agente, PERGUNTA).final_output

print(f"Tipo do objeto retornado: {type(resposta).__name__}")
print(f"categoria_risco: {resposta.categoria_risco}")
print(f"recomendacao: {resposta.recomendacao}")
print(f"confianca: {resposta.confianca}")

# Montagem do arquivo Markdown
linhas = [
    "# Respostas do agente_saida_estruturada",
    "",
    f"Execução registrada em {datetime.now():%d/%m/%Y às %H:%M}.",
    "",
    "## Instruções do agente",
    "",
    *(f"> {linha}" for linha in INSTRUCOES.splitlines()),
    "",
    "## Pergunta 1",
    "",
    f"**Pergunta:** {PERGUNTA}",
    "",
    "**Resposta do agente:**",
    "",
    f"> **Categoria de risco:** {resposta.categoria_risco}",
    f"> **Recomendação:** {resposta.recomendacao}",
    f"> **Confiança:** {resposta.confianca}",
    "",
]

Path("respostas_segundo_agente.md").write_text(
    "\n".join(linhas),
    encoding = "utf-8"
)
