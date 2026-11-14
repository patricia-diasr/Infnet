# Agente de IA x chatbot x software baseado em regras

## 1. Características que diferenciam um agente

| Característica | Software baseado em regras | Chatbot tradicional | Agente de IA |
| --- | --- | --- | --- |
| **Autonomia na escolha dos passos** | Nenhuma, segue regras escritas à mão, na ordem prevista | Baixa, responde à mensagem atual, sem planejar etapas | Alta, recebe um objetivo e decide os próximos passos |
| **Uso de ferramentas e ação** | Executa apenas as ações programadas em cada regra | Normalmente só gera texto | Pode chamar ferramentas, modelos, consultas, APIs, e usar o resultado |
| **Raciocínio em várias etapas** | Cada regra é avaliada de forma isolada e fixa | Cada turno é praticamente independente | Repete o ciclo perceber-raciocinar-agir até cumprir o objetivo |
| **Situações não previstas** | Falha ou cai em uma regra padrão | Responde de forma genérica ou pede para reformular | Generaliza, interpreta o pedido e adapta o caminho |
| **Saída para outros sistemas** | Fixa, definida na regra | Texto livre para uma pessoa ler | Pode produzir saída estruturada e validável por código |

## 2. Por que o componente de análise de churn deve ser um agente

- A pergunta é aberta e varia a cada uso, o time de retenção pode perguntar sobre um assinante, comparar perfis ou pedir uma priorização. Um software de regras exigiria prever cada variação no código.
- A resposta exige reunir informações de fontes diferentes, o perfil do assinante, a probabilidade do modelo e a política de retenção. Um chatbot só conversa, e o agente decide o que buscar e usa ferramentas para isso.
- A decisão envolve julgamento sobre custos assimétricos, o modelo com o limiar padrão desenvolvido no TP2 deixou passar 419 dos 421 cancelamentos do teste, e baixar o limiar aumenta a cobertura ao custo de mais alertas falsos. Escolher e justificar um ponto de operação é um raciocínio de várias etapas, e não uma resposta pronta.
- A saída precisa ser acionável, o painel da retenção consome categoria de risco, recomendação e confiança em um formato previsível, e não texto livre. O agente pode produzir essa saída estruturada e validável.
- Muitos usuários consultam ao mesmo tempo, o agente é executado de forma assíncrona para atender várias solicitações simultâneas sem bloquear o painel.

Por isso o componente é projetado como agente, o que se espera dele é concluir uma tarefa, e não apenas conversar sobre ela.

## 3. Caso de uso em que um chatbot simples seria suficiente

Um caso de uso seria para responder perguntas frequentes sobre a política de cancelamento, como prazo para cancelar, como cancelar pelo aplicativo ou regras de reembolso. O conteúdo é conhecido e estável, a resposta é o mesmo texto para qualquer assinante, e não há necessidade de consultar dados individuais, usar ferramentas nem executar ações. Um chatbot, ou até uma página de perguntas frequentes, resolveria o caso, e um agente só acrescentaria complexidade e custo sem entregar valor extra.
