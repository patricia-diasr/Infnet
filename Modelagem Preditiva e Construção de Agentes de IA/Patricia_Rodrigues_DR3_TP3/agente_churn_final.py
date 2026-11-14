import asyncio
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from pipeline_final_churn import COLUNAS_FEATURES, carregar_base, treinar_pipeline

load_dotenv()

CATEGORIAS_VALIDAS = {"baixo", "médio", "alto", "indeterminado"}

class RespostaAgente(BaseModel):
    categoria_risco: str = Field(
        description = "Categoria de risco de churn: baixo, médio, alto ou indeterminado (quando não há dados do assinante)."
    )
    recomendacao: str = Field(
        description = "Ação recomendada ao time de retenção, em uma ou duas frases."
    )
    confianca: float = Field(
        description = "Confiança na análise, de 0 a 1, de acordo com a informação disponível."
    )


INSTRUCOES = """Você é um analista de risco de churn da NeoStream, uma plataforma de streaming por assinatura.

Dada uma pergunta do time de retenção sobre um assinante, avalie o risco de ele cancelar e recomende uma ação.

Para analisar um assinante, consulte sempre a ferramenta consultar_risco_churn com o identificador citado na pergunta. Ela devolve o perfil do assinante e a probabilidade de churn estimada pelo modelo da NeoStream.

Fatores de risco no modelo de churn da NeoStream:
- menos tempo de assinatura aumenta o risco.
- menor uso médio semanal aumenta o risco.
- mais reclamações aumentam o risco.
- plano, método de pagamento e dispositivo têm pouca influência.

Defina a categoria pela probabilidade de churn: baixo abaixo de 15%, médio entre 15% e 30%, alto acima de 30%. Na recomendação, cite os fatores do perfil que mais pesam no risco.

Use somente as informações da pergunta e da ferramenta e não invente dados. Se a ferramenta não encontrar o assinante ou a pergunta não trouxer um identificador, use a categoria indeterminado, uma confiança baixa e diga na recomendação que o identificador precisa ser verificado."""

PERGUNTAS = [
    "Qual o risco de o assinante AST-02384 cancelar? O que devemos fazer?",
    "O time de retenção quer saber se vale oferecer desconto ao assinante AST-01015. Qual o risco de churn dele?",
    "Preciso priorizar a campanha de hoje: qual o risco de churn do assinante AST-00026 e que ação você recomenda?",
    "O assinante AST-00066 está conosco há bastante tempo. Ele corre risco de cancelar?",
    "E o assinante AST-99999, qual o risco de churn dele?",
]

base = carregar_base()
pipeline_final = treinar_pipeline(base)[0]

@function_tool
def consultar_risco_churn(cliente_id: str) -> dict:
    """Consulta o perfil de um assinante e a probabilidade de churn estimada pelo modelo da NeoStream.

    Args:
        cliente_id: Identificador do assinante, no formato AST-00000.
    """
    assinante = base[base["cliente_id"] == cliente_id]
    if assinante.empty:
        return {"erro": f"Assinante {cliente_id} não encontrado na base."}

    perfil = assinante[COLUNAS_FEATURES].to_dict(orient = "records")[0]
    probabilidade = pipeline_final.predict_proba(assinante[COLUNAS_FEATURES])[0, 1]

    return {
        "cliente_id": cliente_id,
        **perfil,
        "probabilidade_churn": round(float(probabilidade), 3),
    }


agente = Agent(
    name = "Analista de risco de churn",
    instructions = INSTRUCOES,
    tools = [consultar_risco_churn],
    output_type = RespostaAgente,
)

async def consultar_agente(pergunta):
    resultado = await Runner.run(agente, pergunta)
    chamadas = [
        f"{item.raw_item.name}({item.raw_item.arguments})"
        for item in resultado.new_items
        if item.type == "tool_call_item"
    ]

    return resultado.final_output, chamadas


def validar_resposta(resposta):
    problemas = []
    try:
        RespostaAgente.model_validate(resposta.model_dump(), strict = True)

    except ValidationError:
        problemas.append("esquema Pydantic")

    if resposta.categoria_risco.strip().lower() not in CATEGORIAS_VALIDAS:
        problemas.append("categoria fora de baixo, médio, alto e indeterminado")

    if not 0 <= resposta.confianca <= 1:
        problemas.append("confiança fora do intervalo de 0 a 1")

    if not resposta.recomendacao.strip():
        problemas.append("recomendação vazia")

    return problemas

async def main():
    respostas = await asyncio.gather(*(consultar_agente(p) for p in PERGUNTAS))

    tabela = [
        "| Pergunta | Chamadas à ferramenta | Categoria | Confiança | Recomendação |",
        "|---|---|---|---|---|",
    ]

    for numero, (pergunta, (resposta, chamadas)) in enumerate(
        zip(PERGUNTAS, respostas), start = 1
    ):
        problemas = validar_resposta(resposta)
        chamadas_texto = "; ".join(chamadas) if chamadas else "nenhuma"
        print(f"P{numero}: {pergunta}")
        print(f"  chamadas à ferramenta: {chamadas_texto}")
        print(f"  categoria_risco: {resposta.categoria_risco}")
        print(f"  confianca: {resposta.confianca}")
        print(f"  recomendacao: {resposta.recomendacao}")
        print(f"  validação: {'ok' if not problemas else ', '.join(problemas)}\n")

        recomendacao = resposta.recomendacao.replace("|", "/").replace("\n", " ")
        tabela.append(
            f"| P{numero} | {chamadas_texto} | {resposta.categoria_risco} "
            f"| {resposta.confianca} | {recomendacao} |"
        )

    print("Tabela para o documento de design:")
    print("\n".join(tabela))

if __name__ == "__main__":
    asyncio.run(main())
