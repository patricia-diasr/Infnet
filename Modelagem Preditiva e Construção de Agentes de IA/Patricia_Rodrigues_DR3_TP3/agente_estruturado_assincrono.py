import asyncio
from datetime import datetime
from pathlib import Path
from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

CATEGORIAS_VALIDAS = {"baixo", "médio", "alto"}

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
    "Um assinante do plano premium tem 1 mês de assinatura, usa em média 2 horas por semana e já fez 4 reclamações. Qual o risco de ele cancelar e o que devemos fazer?",
    "Um assinante do plano padrão tem 36 meses de assinatura, usa em média 14 horas por semana e nunca fez reclamações. Qual o risco de ele cancelar e o que devemos fazer?",
    "O modelo estimou 22% de probabilidade de churn para um assinante do plano padrão, com 12 meses de assinatura, 8 horas de uso semanal e 1 reclamação. "
    "Qual a categoria de risco e o que devemos fazer?",
]

agente = Agent(
    name = "Analista de risco de churn",
    instructions = INSTRUCOES,
    output_type = RespostaAgente,
)


async def consultar_agente(pergunta):
    resultado = await Runner.run(agente, pergunta)
    return resultado.final_output


def validar_resposta(resposta):
    try:
        RespostaAgente.model_validate(resposta.model_dump(), strict = True)
        esquema_valido = True

    except ValidationError:
        esquema_valido = False

    return {
        "esquema Pydantic (campos e tipos)": esquema_valido,
        "categoria entre baixo, médio e alto": resposta.categoria_risco.strip().lower()
        in CATEGORIAS_VALIDAS,
        "confiança entre 0 e 1": 0 <= resposta.confianca <= 1,
        "recomendação preenchida": bool(resposta.recomendacao.strip()),
    }


async def main():
    respostas = await asyncio.gather(*(consultar_agente(p) for p in PERGUNTAS))
    validacoes = [validar_resposta(resposta) for resposta in respostas]
    todas_validas = all(all(checagens.values()) for checagens in validacoes)

    for numero, (resposta, checagens) in enumerate(zip(respostas, validacoes), start = 1):
        print(f"Resposta {numero}: {type(resposta).__name__} | {checagens}")

    print(f"Todas as respostas válidas: {'sim' if todas_validas else 'não'}")

    nomes_checagens = list(validacoes[0])
    linhas = [
        "# Validação da saída estruturada",
        "",
        f"Execução registrada em {datetime.now():%d/%m/%Y às %H:%M}, com {len(PERGUNTAS)} perguntas executadas de forma assíncrona (`asyncio.gather`).",
        "",
        "## Verificações aplicadas a cada objeto `RespostaAgente`",
        "",
        "- **Esquema Pydantic:** o objeto é revalidado com `RespostaAgente.model_validate(..., strict=True)`, que falha se houver campo ausente ou de tipo incorreto (`str`, `str` e `float`).",
        "- **Categoria:** o valor de `categoria_risco` deve ser baixo, médio ou alto.",
        "- **Confiança:** o valor de `confianca` deve estar entre 0 e 1.",
        "- **Recomendação:** o texto de `recomendacao` não pode estar vazio.",
        "",
        "## Resultado por resposta",
        "",
        "| Resposta | " + " | ".join(nomes_checagens) + " |",
        "|---|" + "---|" * len(nomes_checagens),
        *(
            f"| {numero} | "
            + " | ".join(
                "OK" if aprovado else "FALHA" for aprovado in checagens.values()
            )
            + " |"
            for numero, checagens in enumerate(validacoes, start = 1)
        ),
        "",
        f"**Conclusão:** {'todas as respostas respeitam o esquema e as regras verificadas.' if todas_validas else 'há respostas que não respeitam o esquema ou alguma regra verificada (veja as linhas com FALHA).'}",
        "",
        "## Objetos retornados",
        "",
    ]

    for numero, (pergunta, resposta) in enumerate(zip(PERGUNTAS, respostas), start = 1):
        linhas += [
            f"### Resposta {numero}",
            "",
            f"**Pergunta:** {pergunta}",
            "",
            *(
                f"- **{campo}:** {valor}"
                for campo, valor in resposta.model_dump().items()
            ),
            "",
        ]

    Path("validacao_saida_estruturada.md").write_text(
        "\n".join(linhas), encoding = "utf-8"
    )

if __name__ == "__main__":
    asyncio.run(main())
