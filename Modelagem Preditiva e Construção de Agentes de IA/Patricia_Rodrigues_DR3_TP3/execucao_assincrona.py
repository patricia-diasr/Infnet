import asyncio
import time
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

PERGUNTAS = [
    "Um assinante do plano básico tem 2 meses de assinatura, usa em média 3 horas por semana e já fez 3 reclamações. Qual o risco de ele cancelar e o que devemos fazer?",
    "Um assinante do plano padrão tem 36 meses de assinatura, usa em média 14 horas por semana e nunca fez reclamações. Qual o risco de ele cancelar e o que devemos fazer?",
]

agente = Agent(
    name = "Analista de risco de churn",
    instructions = INSTRUCOES,
    output_type = RespostaAgente,
)

async def consultar_agente(pergunta):
    inicio = time.perf_counter()
    resultado = await Runner.run(agente, pergunta)
    return resultado.final_output, time.perf_counter() - inicio


async def main():
    inicio = time.perf_counter()
    concorrentes = await asyncio.gather(*(consultar_agente(p) for p in PERGUNTAS))
    tempo_concorrente = time.perf_counter() - inicio
    inicio = time.perf_counter()

    for pergunta in PERGUNTAS:
        await consultar_agente(pergunta)

    tempo_sequencial = time.perf_counter() - inicio
    estimativa_sequencial = sum(duracao for _, duracao in concorrentes)

    print(f"Tempo total concorrente: {tempo_concorrente:.2f} s")
    print(f"Tempo total sequencial (medido): {tempo_sequencial:.2f} s")
    print(f"Estimativa sequencial (soma das durações): {estimativa_sequencial:.2f} s")

    linhas = [
        "# Execução assíncrona do agente",
        "",
        f"Execução registrada em {datetime.now():%d/%m/%Y às %H:%M}, com {len(PERGUNTAS)} chamadas ao agente.",
        "",
        "## Tempos medidos",
        "",
        "| Forma de execução | Tempo total |",
        "|---|---|",
        f"| Concorrente, com `asyncio.gather` (medido) | {tempo_concorrente:.2f} s |",
        f"| Sequencial, uma chamada após a outra (medido) | {tempo_sequencial:.2f} s |",
        f"| Estimativa sequencial (soma das durações individuais da execução concorrente) | {estimativa_sequencial:.2f} s |",
        "",
        f"Razão entre o tempo sequencial medido e o concorrente: {tempo_sequencial / tempo_concorrente:.2f}x.",
        "",
        "## Respostas e duração de cada chamada (execução concorrente)",
        "",
    ]

    for numero, (pergunta, (resposta, duracao)) in enumerate(
        zip(PERGUNTAS, concorrentes), start = 1
    ):
        linhas += [
            f"### Chamada {numero} ({duracao:.2f} s)",
            "",
            f"**Pergunta:** {pergunta}",
            "",
            *(
                f"- **{campo}:** {valor}"
                for campo, valor in resposta.model_dump().items()
            ),
            "",
        ]

    Path("execucao_assincrona.md").write_text("\n".join(linhas), encoding = "utf-8")

if __name__ == "__main__":
    asyncio.run(main())
