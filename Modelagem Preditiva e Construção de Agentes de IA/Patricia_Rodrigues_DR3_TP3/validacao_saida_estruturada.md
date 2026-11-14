# Validação da saída estruturada

Execução registrada em 14/11/2026 às 12:29, com 3 perguntas executadas de forma assíncrona (`asyncio.gather`).

## Verificações aplicadas a cada objeto `RespostaAgente`

- **Esquema Pydantic:** o objeto é revalidado com `RespostaAgente.model_validate(..., strict=True)`, que falha se houver campo ausente ou de tipo incorreto (`str`, `str` e `float`).
- **Categoria:** o valor de `categoria_risco` deve ser baixo, médio ou alto.
- **Confiança:** o valor de `confianca` deve estar entre 0 e 1.
- **Recomendação:** o texto de `recomendacao` não pode estar vazio.

## Resultado por resposta

| Resposta | esquema Pydantic (campos e tipos) | categoria entre baixo, médio e alto | confiança entre 0 e 1 | recomendação preenchida |
|---|---|---|---|---|
| 1 | OK | OK | OK | OK |
| 2 | OK | OK | OK | OK |
| 3 | OK | OK | OK | OK |

**Conclusão:** todas as respostas respeitam o esquema e as regras verificadas.

## Objetos retornados

### Resposta 1

**Pergunta:** Um assinante do plano premium tem 1 mês de assinatura, usa em média 2 horas por semana e já fez 4 reclamações. Qual o risco de ele cancelar e o que devemos fazer?

- **categoria_risco:** alto
- **recomendacao:** Priorizar contato de retenção, investigar e resolver as 4 reclamações e incentivar maior uso da plataforma. Não há probabilidade estimada pelo modelo, portanto a avaliação é qualitativa.
- **confianca:** 0.9

### Resposta 2

**Pergunta:** Um assinante do plano padrão tem 36 meses de assinatura, usa em média 14 horas por semana e nunca fez reclamações. Qual o risco de ele cancelar e o que devemos fazer?

- **categoria_risco:** baixo
- **recomendacao:** O assinante apresenta baixo risco, dado o longo tempo de assinatura, uso semanal elevado e ausência de reclamações. Mantenha o acompanhamento e ações gerais de engajamento; não há dados de probabilidade estimada ou histórico de tendência recente.
- **confianca:** 0.88

### Resposta 3

**Pergunta:** O modelo estimou 22% de probabilidade de churn para um assinante do plano padrão, com 12 meses de assinatura, 8 horas de uso semanal e 1 reclamação. Qual a categoria de risco e o que devemos fazer?

- **categoria_risco:** médio
- **recomendacao:** Realizar uma ação de retenção preventiva, acompanhando o engajamento e buscando entender a reclamação registrada. A probabilidade estimada é suficiente para atenção, embora os dados disponíveis não indiquem alto risco.
- **confianca:** 0.96
