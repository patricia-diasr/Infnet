# Justificativa de design do agente de análise de churn

## 1. Visão geral

O agente final `agente_churn_final.py` recebe perguntas do time de retenção da NeoStream sobre assinantes específicos, identificados pelo código, e devolve para cada uma uma resposta estruturada com categoria de risco, recomendação de ação e confiança. Ele reúne os primitivos dos Exercícios 4 a 7 e acrescenta uma ferramenta que consulta o pipeline de churn do TP1.

A base de assinantes `assinantes_neostream.csv` é é gerada automaticamente, com semente fixa, quando não existe na pasta.

## 2. Decisões de design

### 2.1 Uso de `Agent` e `Runner`

**Por que é necessário neste caso de uso:**

- O time de retenção faz perguntas abertas sobre assinantes diferentes, em linguagem natural. O modelo de churn do TP2 apenas devolve uma classe ou uma probabilidade para um vetor de features já pronto, e não responde "o que devemos fazer com este assinante?". O `Agent`, guiado por instruções, interpreta a pergunta e produz a análise.
- As instruções do `Agent` concentram o conhecimento de domínio, o papel de analista de risco, os fatores de risco observados no TP2, como menos o tempo de assinatura, menos uso e mais reclamações aumentam o risco, já o plano, o pagamento e o dispositivo pesam pouco, as faixas de categoria, com baixo abaixo de 15%, médio entre 15% e 30%, alto acima de 30%, e as regras de não inventar dados e de tratar assinantes não encontrados.
- O `Runner` executa o agente e conduz o ciclo, ele chama o modelo, executa as ferramentas que o modelo pedir, devolve os resultados e decide quando a execução terminou. Sem ele, seria preciso escrever à mão a chamada ao modelo, o laço de chamadas de ferramenta e a conversão da saída.

### 2.2 Ferramenta que consulta o pipeline do TP1

**Por que é necessário neste caso de uso:**

- As perguntas do time de retenção citam apenas o identificador do assinante. Para responder, o agente precisa do perfil e da probabilidade de churn, e sem uma ferramenta essas informações teriam de ser consultadas e coladas na pergunta por uma pessoa, ou o agente as inventaria.
- A ferramenta `consultar_risco_churn` busca o assinante na base e calcula a probabilidade com o mesmo pipeline do TP1, de modo que o agente usa o modelo já validado em vez de estimar o risco por conta própria.
- A ferramenta devolve apenas o perfil e a probabilidade, e não o rótulo real de cancelamento, para que a resposta do agente venha da análise e não de um dado que não existiria em produção.
- Quando o identificador não existe, a ferramenta devolve uma mensagem de erro em vez de falhar, e as instruções mandam o agente responder com a categoria `indeterminado` e confiança baixa, pedindo a verificação do identificador.

### 2.3 Saída estruturada com Pydantic

**Por que é necessário neste caso de uso:**

- O painel da retenção exibe categoria de risco e recomendação. Se a saída fosse texto livre, alguém ou algum código teria de interpretá-la, e qualquer variação de formato quebraria a integração.
- O esquema `RespostaAgente` fixa o contrato, `categoria_risco` (texto), `recomendacao` (texto) e `confianca` (número). A descrição de cada campo orienta o modelo sobre o que preencher, e a categoria `indeterminado` permite representar o caso sem dados sem forçar um valor falso.
- A validação é feita em duas camadas, o SDK entrega o objeto já no formato do esquema, e a função `validar_resposta` confere as regras de negócio que o tipo não expressa, a categoria deve ser baixo, médio, alto ou indeterminado, a confiança deve estar entre 0 e 1 e a recomendação não pode estar vazia.
- Como limitação, a validação garante o formato e as regras, mas não que a análise do modelo esteja correta.

### 2.4 Execução assíncrona

**Por que é necessário neste caso de uso:**

- O painel recebe solicitações de vários usuários ao mesmo tempo, e cada execução do agente, com a espera do modelo e da ferramenta, bloquearia o painel na versão síncrona.
- Com `Runner.run` e `asyncio.gather`, as cinco perguntas do teste foram executadas ao mesmo tempo. A medição comparando a execução concorrente com a sequencial está em `execucao_assincrona.md`.
- O `gather` devolve os resultados na ordem das perguntas, o que permite associar cada resposta ao assinante correto.

### 2.5 Outras decisões

- **Base gerada automaticamente com semente fixa:** a base é sintética e não há onde baixá-la. Gerá-la com a mesma semente do TP1 produz sempre o mesmo arquivo e torna o ZIP reproduzível em qualquer máquina.
- **Pipeline treinado ao iniciar:** o agente treina o pipeline do TP1 a cada execução, o que evita depender de um modelo salvo em arquivo.
- **Faixas de 15% e 30%:** são uma escolha de design, apoiada nos limiares analisados no TP2, e podem ser recalibradas com o time financeiro.
- **Chave de API em variável de ambiente:** a chave fica no `.env`, e o `.env.example` traz apenas o nome da variável.

## 3. Diferenciação frente a um chatbot

| Aspecto | Chatbot tradicional | Agente de análise de churn |
| --- | --- | --- |
| **Objetivo** | Conversar e responder à mensagem atual | Concluir uma tarefa: diagnosticar o risco e recomendar uma ação |
| **Informação** | Responde com o que sabe ou com o texto da conversa | Decide consultar uma ferramenta e usa o resultado (perfil e probabilidade do pipeline) |
| **Saída** | Texto livre para uma pessoa ler | Objeto `RespostaAgente` validado, consumível pelo painel |
| **Papel e limites** | Genéricos | Papel, fatores de risco, faixas de categoria e regras para dados ausentes definidos nas instruções |
| **Volume** | Em geral, uma conversa por vez | Várias solicitações simultâneas, de forma assíncrona |

## 4. Relação com o ciclo perceber-raciocinar-agir e comportamento observado

### 4.1 Resultado da execução do agente final

Perguntas executadas:

- **P1:** "Qual o risco de o assinante AST-02384 cancelar? O que devemos fazer?"
- **P2:** "O time de retenção quer saber se vale oferecer desconto ao assinante AST-01015. Qual o risco de churn dele?"
- **P3:** "Preciso priorizar a campanha de hoje: qual o risco de churn do assinante AST-00026 e que ação você recomenda?"
- **P4:** "O assinante AST-00066 está conosco há bastante tempo. Ele corre risco de cancelar?"
- **P5:** "E o assinante AST-99999, qual o risco de churn dele?"

| Pergunta | Chamadas à ferramenta | Categoria | Confiança | Recomendação |
| --- | --- | --- | --- | --- |
| P1 | consultar_risco_churn({"cliente_id":"AST-02384"}) | alto | 0.98 | Priorizar contato de retenção: o principal fator é o tempo de assinatura muito curto (0,3 mês), agravado por 2 reclamações. O uso médio semanal de 6,4 horas é relativamente positivo, portanto investigue e resolva as reclamações. |
| P2 | consultar_risco_churn({"cliente_id":"AST-01015"}) | alto | 0.98 | Vale considerar oferecer desconto: a probabilidade de churn é 34,6%. Os principais fatores são o tempo de assinatura relativamente curto (7,4 meses), uso semanal de 8,8 horas e 2 reclamações. |
| P3 | consultar_risco_churn({"cliente_id":"AST-00026"}) | médio | 0.98 | Priorize uma ação de retenção personalizada, pois o risco é de 22,3%. Os principais fatores são o tempo de assinatura de 8,8 meses e o uso médio semanal de 10,8 horas; há apenas 1 reclamação. |
| P4 | consultar_risco_churn({"cliente_id":"AST-00066"}) | baixo | 0.99 | O risco de cancelamento é baixo (4,9%). O longo tempo de assinatura (47,6 meses), uso semanal de 7,7 horas e ausência de reclamações favorecem a retenção; não há necessidade de intervenção imediata. |
| P5 | consultar_risco_churn({"cliente_id":"AST-99999"}) | indeterminado | 0.98 | O assinante AST-99999 não foi encontrado na base. Verifique o identificador antes de avaliar o risco de churn. |

A validação programática (`validar_resposta`) retornou `ok` nas cinco respostas.

### 4.2 O ciclo no comportamento observado

- **Perceber:** em cada pergunta, o agente percebeu apenas o identificador do assinante e o pedido do time de retenção. Ele não recebeu o perfil nem a probabilidade: essas informações só chegaram depois, como resultado da ferramenta.
- **Agir (primeira ação):** em todas as cinco perguntas, o agente decidiu chamar a ferramenta `consultar_risco_churn` uma única vez, passando o identificador citado na pergunta (por exemplo, `{"cliente_id":"AST-02384"}`), como mostra a coluna "Chamadas à ferramenta".
- **Perceber (resultado) e raciocinar:** com o perfil e a probabilidade em mãos, o agente definiu a categoria. As probabilidades de 44,6%, 34,6%, 22,3% e 4,9% resultaram em risco alto, alto, médio e baixo, coerente com as faixas das instruções (baixo abaixo de 15%, médio entre 15% e 30%, alto acima de 30%). As recomendações citam dados do perfil: em P1, o tempo de assinatura muito curto (0,3 mês) e as 2 reclamações; em P4, o longo tempo de assinatura (47,6 meses) e a ausência de reclamações.
- **Agir (resposta final):** o agente produziu a resposta estruturada, e a validação deu `ok` nas cinco respostas, então o painel pode consumir os campos sem interpretar texto.
- **Caso de erro (P5):** o identificador AST-99999 não existe, e a ferramenta devolveu um erro. O agente respondeu com a categoria `indeterminado` e a recomendação de verificar o identificador antes de avaliar o risco, sem inventar dados.

### 4.3 Limites observados no comportamento do agente

- **Confiança no caso sem dados:** as instruções pediam confiança baixa para `indeterminado`, mas em P5 o agente informou 0,98. Ele tratou o campo como a certeza de que o assinante não existe na base, e não como a confiança na avaliação de risco. A validação não detecta isso, pois só verifica se o valor está entre 0 e 1.
- **Confiança pouco informativa:** o campo variou apenas entre 0,98 e 0,99 nas cinco respostas. Ele é declarado pelo próprio modelo de linguagem e não é calibrado, ao contrário da probabilidade do pipeline.
- **Interpretação dos fatores de uso:** a base tem média e mediana de 9,0 horas de uso por semana. Mesmo assim, em P1 o uso de 6,4 horas é chamado de "relativamente positivo" (abaixo da média), em P2 e P3 os usos de 8,8 e 10,8 horas aparecem entre os "principais fatores" de risco, e em P4 as 7,7 horas aparecem entre os fatores que favorecem a retenção. As instruções indicam a direção de cada fator, mas não trazem valores de referência, e o agente não tem como saber o que é pouco ou muito uso. A categoria de risco não foi afetada, pois vem da probabilidade da ferramenta, mas o texto da recomendação pode induzir o time de retenção a uma leitura errada.

### 4.4 O que o comportamento observado mostra sobre o ciclo

Diferentemente de um script de entrada fixa, o agente percorreu o ciclo mais de uma vez em cada pergunta: percebeu a pergunta, agiu chamando a ferramenta, percebeu o resultado da ação e só então raciocinou e respondeu. A decisão de consultar a ferramenta, e com qual argumento, partiu do próprio agente, a partir da pergunta em linguagem natural, e o caso do identificador inexistente mostra o agente reagindo ao resultado de uma ação em vez de falhar. Ainda assim, o ciclo observado é curto, há uma única ferramenta e o agente não precisou replanejar. Os limites da seção 4.3 indicam onde o raciocínio do agente depende da qualidade das instruções, o que aponta os próximos ajustes de design.
