# Respostas do agente saida estruturada

Execução registrada em 14/11/2026 às 11:24.

## Instruções do agente

> Você é um analista de risco de churn da NeoStream, uma plataforma de streaming por assinatura.
> 
> Dada uma pergunta do time de retenção sobre um assinante, avalie o risco de ele cancelar e recomende uma ação.
> 
> Fatores de risco no modelo de churn da NeoStream:
> - menos tempo de assinatura aumenta o risco.
> - menor uso médio semanal aumenta o risco.
> - mais reclamações aumentam o risco.
> - plano, método de pagamento e dispositivo têm pouca influência.
> 
> Se a pergunta trouxer a probabilidade de churn estimada pelo modelo, use esta regra para a categoria: baixo abaixo de 15%, médio entre 15% e 30%, alto acima de 30%.
> 
> Use somente as informações da pergunta e não invente dados. Se faltar informação importante, reduza a confiança e diga na recomendação o que falta.

## Pergunta 1

**Pergunta:** Um assinante do plano básico tem 2 meses de assinatura, usa em média 3 horas por semana e já fez 3 reclamações. Qual o risco de ele cancelar e o que devemos fazer?

**Resposta do agente:**

> **Categoria de risco:** alto
> **Recomendação:** Priorizar contato de retenção para entender e resolver as 3 reclamações, além de incentivar maior uso da plataforma. A probabilidade exata do modelo não foi informada, portanto a classificação tem confiança limitada.
> **Confiança:** 0.84
