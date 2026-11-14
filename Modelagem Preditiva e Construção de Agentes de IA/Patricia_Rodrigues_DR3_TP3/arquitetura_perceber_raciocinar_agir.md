# Arquitetura do componente de análise de churn: ciclo perceber-raciocinar-agir

## 1. Contexto

O time de retençao da NeoStream solicitou que um componente que consiga processar uma pergunta em linguagem natural, decidir quais informações são nescessárias e produzir uma resposta fundamentada nelas. Para isso, não é possível usar o modelo de churn desenvolvido no TP2, já que ele apenas devolve uma classe ou uma probabilidade para um conjunto de features já definidas, sendo preciso que esse componente seja um agente de IA com um ciclo de perceber-raciocinar-agir.

## 2. O ciclo aplicado ao time de retenção

### 2.1 Perceber

O que o componente recebe e observa:

- A pergunta feita pelo analista de retenção, em linguagem natural e sem um formato fixo.
- O perfil do assinante citado, com informações como plano, tempo de assinatura, uso médio semanal e número de reclamações.
- O sinal do modelo de churn, ou seja, a probabilidade de cancelamento estimada para aquele assinante.
- O contexto da política de retenção, como as ações e os descontos disponíveis.
- O resultado de qualquer consulta feita ao longo da própria execução.

### 2.2 Raciocinar

Sobre o que o componente raciocina:

- A intenção da pergunta, considerando o analista quer, seja um diagnóstico de um assinante, uma comparação, uma priorização ou outro.
- O que falta na pergunta, por exemplo, se o perfil ou a probabilidade de churn não foram informados, é preciso obtê-los antes de concluir.
- A evidência disponível, como a probabilidade do modelo e os fatores observados no perfil.
- O custo que pode ser gerado por erros, deixar passar um cancelamento costuma custar mais do que oferecer um desconto desnecessário.
- A conclusão chegada, com a categoria de risco, a ação mais adequada e o grau de confiança na resposta.

### 2.3 Agir

A ação tomada pelo componente:

- Consultar as fontes de informação que faltam, por exemplo, executar o modelo de churn para o assinante em questão.
- Responder de forma estruturada, com categoria de risco, recomendação de ação e confiança, para que o painel da retenção consuma a resposta sem interpretação manual.
- Repetir o ciclo caso o resultado de uma ação revele uma nova lacuna, o resultado volta a ser percebido e o componente raciocina de novo antes de concluir.

## 3. Comparação com o fluxo de um script tradicional

| Aspecto | Script tradicional (ex.: `pipeline.predict`) | Agente de análise de churn |
| --- | --- | --- |
| **Entrada** | Fixa e estruturada, um vetor com as features, na ordem e no formato esperados | Pergunta em linguagem natural, de formato aberto |
| **Controle de fluxo** | Definido em tempo de programação, uma sequência linear de passos, sempre a mesma | Decidido em tempo de execução, o agente escolhe os próximos passos e repete o ciclo até cumprir o objetivo |
| **Informação ausente** | Gera erro ou resultado inválido | Identifica a lacuna e busca ou pede a informação antes de concluir |
| **Saída** | Um valor fixo, como 0 ou 1, ou uma probabilidade, sem explicação | Resposta fundamentada, com justificativa, recomendação e confiança |
| **Previsibilidade** | Determinístico, a mesma entrada gera sempre a mesma saída | Probabilístico, a resposta pode variar, o que exige validar o formato da saída |

As duas diferenças mais importantes são o controle de fluxo, decidido pelo agente durante a execução, e não fixado no código, e o tratamento de informação ausente, em que o agente reage a lacunas em vez de falhar. São elas que permitem atender uma pergunta aberta do time de retenção sem que cada variação da pergunta precise ser prevista no código.
