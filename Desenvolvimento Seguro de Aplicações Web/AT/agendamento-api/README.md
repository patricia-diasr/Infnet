# agendamento-api

API REST para digitalização do agendamento de consultas de uma rede de clínicas médicas, construída como Assessment da disciplina de Desenvolvimento Seguro de Aplicações Web.

## Contexto

A aplicação gerencia três recursos centrais, **pacientes**, **profissionais de saúde** e **consultas**, e atende três tipos de cliente:

- uma aplicação frontend que consome a API em JSON;
- uma página HTML interna (`/agenda-html`), usada pela recepção das clínicas para consultar a agenda do dia;
- um laboratório de exames parceiro, que integra via comunicação máquina-a-máquina (M2M) para consultar horários disponíveis.

## Papéis e modelo de autorização

O sistema distingue três papéis, cada um com permissões diferentes sobre os mesmos recursos:

| Papel | Permissões |
| --- | --- |
| **recepcionista** | Acesso de leitura a todas as consultas (agenda completa); não cria nem edita consultas |
| **profissional** | Cria consultas; lê e gerencia (edita/cancela) apenas as consultas dos próprios pacientes |
| **administrador** | Acesso total de leitura e escrita a todas as consultas; único papel com acesso a `GET /usuarios`; login exige MFA |

O modelo de autorização é um híbrido de **RBAC** (permissões gerais por papel) e **autorização por recurso / ownership** (um profissional só acessa consultas cujo `profissional_username` corresponde à sua própria conta).

Um laboratório parceiro externo autentica separadamente via **OAuth2 Client Credentials** (fluxo M2M, sem usuário humano envolvido), recebendo apenas o escopo `horarios:leitura`, acesso estruturalmente restrito a um endpoint que nunca retorna dado de paciente, mesmo que o token seja comprometido.

## Estrutura do projeto

```
agendamento-api/
├── .github/workflows/
│   └── security.yml          # pipeline de segurança (SAST, SCA, testes, DAST)
├── app/
│   ├── config.py              # BaseSettings, lê informações do .env
│   ├── rate_limit.py           # instância compartilhada do Limiter (slowapi)
│   ├── models/                 # contratos de dados Pydantic/SQLModel
│   │   ├── usuario.py
│   │   ├── consulta.py
│   │   └── cliente_api.py       # clientes M2M (laboratório parceiro)
│   ├── database/                # camada de persistência (SQLModel + Session)
│   │   ├── session.py            # engine, criar_tabelas(), get_session()
│   │   ├── seed.py                # usuários e cliente M2M de exemplo
│   │   ├── users_db.py
│   │   ├── db.py                  # CRUD de consultas
│   │   └── clients_db.py
│   ├── routes/                   # endpoints HTTP (APIRouter por recurso)
│   │   ├── auth.py                # /token, /token/mfa, /token/client
│   │   ├── usuarios.py
│   │   └── consultas.py
│   └── security/                 # autenticação, autorização, hashing
│       ├── hashing.py              # bcrypt via passlib
│       ├── auth.py                  # JWT, MFA, RBAC, escopos
│       └── ownership.py             # dependency genérica de ownership
├── templates/                    # páginas HTML (Jinja2, autoescape)
├── scripts/
│   └── security_gate.py          # gate usado no pipeline (Bandit + pip-audit)
├── tests/
│   ├── conftest.py                # fixtures: cria tabelas/seed, reseta rate limiter
│   ├── test_consultas.py           # CRUD, ownership, extra=forbid
│   ├── test_auth.py                  # login, MFA, RBAC básico
│   ├── test_m2m.py                    # client credentials, escopos
│   ├── test_agenda_html.py             # proteção da página da recepção
│   ├── test_autorizacao_expandida.py    # vetores adicionais do threat model
│   └── test_unitarios_mocking.py         # testes unitários isolados (mocking)
├── reports/                       # evidências de segurança
├── .env.example                   # variáveis de ambiente esperadas, sem segredo real
├── main.py                        # cria o FastAPI, middlewares, lifespan, exception handler
├── run.py                         # ponto de entrada recomendado para rodar o servidor
└── requirements.txt
```

## Como rodar

```powershell
# ambiente virtual
python -m venv venv
venv\Scripts\Activate.ps1

# dependências
pip install -r requirements.txt

# variáveis de ambiente -- copie o exemplo e ajuste se necessário
copy .env.example .env
```

**Antes de subir o servidor pela primeira vez**, confirme que não existe um `agendamento.db` antigo na pasta. O SQLite/SQLModel cria tabelas que ainda não existem, mas não migra automaticamente um schema já existente, um banco desatualizado causa erros como `no such column`. Se houver um arquivo `agendamento.db`, apague-o:

```powershell
del agendamento.db
```

Suba o servidor com:

```powershell
python run.py
```

*(use `python run.py`, não `uvicorn main:app --reload` diretamente, é o `run.py` que desabilita o cabeçalho `Server`, corrigindo um achado do scan com OWASP ZAP no exercício 13)*

Na primeira subida, o `lifespan` da aplicação cria as tabelas e semeia os usuários de exemplo abaixo, além do cliente M2M do laboratório parceiro.

| username | senha | papel |
| --- | --- | --- |
| `recepcao1` | `senha123` | recepcionista |
| `dra.souza` | `senha456` | profissional |
| `dr.lima` | `senha789` | profissional |
| `admin` | `admin123` | administrador (exige MFA no login) |

Client M2M de exemplo: `client_id=laboratorio-parceiro`, `client_secret=segredo-laboratorio-123`, escopo `horarios:leitura`.

## Onde acessar

Com o servidor rodando em `http://127.0.0.1:8000`:

- `GET /` - status do serviço
- `GET /docs` - Swagger UI (documentação interativa)
- `GET /openapi.json` - especificação OpenAPI
- `POST /token` - login de usuário (recepcionista/profissional/administrador)
- `POST /token/mfa` - confirmação do segundo fator (contas administrativas)
- `POST /token/client` - login M2M (laboratório parceiro)
- `/consultas/*` - CRUD de consultas (autenticado)
- `/consultas/horarios-disponiveis` - disponibilidade por profissional (escopo `horarios:leitura`)
- `/usuarios/*` - cadastro (público) e listagem (só administrador)
- `GET /agenda-html` - agenda do dia da recepção (HTTP Basic Auth, mesmas contas acima)

## Como rodar os testes

```powershell
pytest tests/ -v
```

Se um `agendamento.db` antigo estiver causando erro de schema nos testes, apague-o antes (`del agendamento.db`), o mesmo cuidado da seção "Como rodar" acima se aplica aqui.

## Segurança - resumo dos controles implementados

- **Autenticação:** OAuth2 Bearer + JWT (expiração de 30 min), hashing de senha com `bcrypt`, MFA para contas administrativas com código entregue por canal separado da resposta HTTP (nunca no corpo da resposta de login).
- **Autorização:** RBAC por papel + ownership por recurso; escopos OAuth distintos para usuários humanos (`consultas:leitura`/`escrita`, `usuarios:leitura`) e para o cliente M2M (`horarios:leitura`, apenas).
- **Validação de entrada:** modelos Pydantic/SQLModel com `extra='forbid'` em todos os payloads de escrita; senha limitada a no máximo 72 caracteres (limite do `bcrypt`), fechando a causa raiz de um erro 500 encontrado durante a auditoria com OWASP ZAP (Exercício 13).
- **Tratamento de erros:** handler de exceção global (`main.py`) garante que nenhuma exceção não tratada vaze detalhes internos (stack trace) na resposta ao cliente.
- **Rede:** CORS com allowlist explícita (sem wildcard), cabeçalhos HSTS, X-Frame-Options, X-Content-Type-Options e Content-Security-Policy em toda resposta; cabeçalho `Server` suprimido (ver `run.py`); rate limiting diferenciado (5/min no login, 100/min na listagem de consultas).
- **Persistência:** SQLModel com queries sempre parametrizadas; credenciais de banco e a chave de assinatura JWT geridas via `BaseSettings`/`.env`, nunca hardcoded no código-fonte.
- **Pipeline de segurança:** GitHub Actions (`.github/workflows/security.yml`) rodando SAST (Bandit) e SCA (pip-audit) em todo PR/push, com um security gate customizado (`scripts/security_gate.py`) que bloqueia o pipeline em achados de severidade Alta/Crítica

## Pasta `reports/`

Reúne as evidências de segurança geradas nos exercícios 12 e 13 do Assessment, referenciadas no relatório técnico final:

- **`bandit-report.json`** - saída do SAST (Bandit) rodado contra `app/` e `main.py`.
- **`pip-audit-report.json`** - saída do SCA (pip-audit) rodado contra `requirements.txt`, incluindo o achado de CVE-2024-23342 (pacote `ecdsa`, dependência transitiva de `python-jose`), documentado no relatório como risco aceito.
- **`openapi.json`** - especificação OpenAPI da aplicação no momento da auditoria manual da spec (exercício 13).
- **`zap-report-antes.html`** - primeiro scan passivo do OWASP ZAP, com 10 achados, incluindo um erro 500 real em `POST /usuarios/` (senha excedendo o limite de 72 bytes do bcrypt) que vazava detalhes internos.
- **`zap-report-depois.html`** - scan final do ZAP após as correções (limite de tamanho de senha, handler de exceção global, Content-Security-Policy completa, supressão do cabeçalho `Server`), com apenas 4 achados remanescentes, todos classificados como risco residual aceito no relatório técnico.
- **`assets/`** - recursos estáticos (CSS/imagens) usados pelos relatórios HTML do ZAP acima

## Riscos residuais conhecidos

Documentados em detalhe no relatório técnico do Exercício 13:

1. **CVE-2024-23342** (`ecdsa`, via `python-jose`) - sem correção disponível upstream; risco aceito porque a aplicação usa exclusivamente HS256 (nunca ECDSA) para assinar JWTs.
2. **HTTP Basic Auth em `/agenda-html` sem HTTPS** - aceitável em desenvolvimento; deve ser bloqueante para liberação em produção até a aplicação estar servida atrás de HTTPS/TLS.
3. **`/docs` e `/openapi.json` públicos** - recomendado desabilitar (`docs_url = None, openapi_url = None`) fora do ambiente de desenvolvimento.

Nenhum risco residual remanescente atinge severidade Alta/Crítica nem envolve exposição de dado de paciente sem controle de acesso associado.
