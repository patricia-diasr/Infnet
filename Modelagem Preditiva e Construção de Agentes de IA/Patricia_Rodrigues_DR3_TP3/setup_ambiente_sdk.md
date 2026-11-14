# Configuração do ambiente do OpenAI Agents SDK

## 1. Pré-requisitos

- Python 3.10 ou superior.
- Uma conta na plataforma de API da OpenAI (`platform.openai.com`), separada da conta do ChatGPT, com saldo de crédito.
- Uma chave de API criada em *Settings → API keys → Create new secret key*. A chave é exibida uma única vez, então deve ser copiada na hora.

## 2. Ambiente virtual

Na pasta do projeto, crie um ambiente virtual para isola as bibliotecas do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Instalação do SDK e registro da versão

```powershell
python -m pip install openai-agents python-dotenv pandas scikit-learn
```

As versões instaladas das quatro dependências diretas (`openai-agents`, `python-dotenv`, `pandas` e `scikit-learn`) ficam registradas em `requirements.txt`, com versão fixa, gerado a partir do `pip freeze`. O `pandas` e o `scikit-learn` são necessários porque o agente final usa o pipeline de churn do TP1. Para reproduzir o ambiente em outra máquina:

```powershell
python -m pip install -r requirements.txt
```

## 4. Chave de API como variável de ambiente (`.env` + `python-dotenv`)

O SDK procura a chave na variável de ambiente `OPENAI_API_KEY`. Para não escrever a chave no código, ela fica em um arquivo `.env`, que o `python-dotenv` carrega com `load_dotenv()` no início dos scripts.

1. Copie o modelo: `Copy-Item .env.example .env`.
2. Abra o `.env` e preencha a linha `OPENAI_API_KEY=` com a chave, sem aspas e sem espaços.
3. Nunca escreva a chave em arquivos `.py` ou `.md`.

O arquivo `.env.example` contém apenas o nome da variável, sem valor, e é o único dos dois que acompanha o projeto.

## 5. Verificação do ambiente

```powershell
python verificar_ambiente.py
```

O script confirma, sem exibir a chave, que o pacote `openai-agents` está instalado, que a variável `OPENAI_API_KEY` está definida e que o cliente da OpenAI a leu corretamente. A saída esperada é:

```
Pacote openai-agents instalado: versão <versão instalada>
Variável OPENAI_API_KEY definida: sim
Cliente da OpenAI leu a chave do ambiente: True
```

## 6. Ordem de execução dos scripts

Com o ambiente ativado e o `.env` preenchido:

| Ordem | Script | Arquivo gerado |
| --- | --- | --- |
| 1 | `verificar_ambiente.py` | (apenas saída no terminal) |
| 2 | `primeiro_agente.py` | `respostas_primeiro_agente.md` |
| 3 | `agente_saida_estruturada.py` | `respostas_agente_saida_estruturada.md` |
| 4 | `execucao_assincrona.py` | `execucao_assincrona.md` |
| 5 | `agente_estruturado_assincrono.py` | `validacao_saida_estruturada.md` |
| 6 | `pipeline_final_churn.py` (opcional, mostra o pipeline do TP1 sozinho) | `assinantes_neostream.csv` (na primeira execução) |
| 7 | `agente_churn_final.py` | (saída no terminal, com a tabela usada no documento de design) |

## 7. Base de dados e pipeline do TP1

A base `assinantes_neostream.csv` é sintética, ela é gerada pelo código do TP1, com semente fixa, e por isso o conteúdo é sempre o mesmo. O `pipeline_final_churn.py` cria o CSV automaticamente, na pasta em que o script é executado, quando ele ainda não existe. O `agente_churn_final.py` importa esse módulo, e a cada execução treina o pipeline antes de iniciar o agente, o que leva alguns segundos.
