# eventos-api

API REST em FastAPI para gerenciamento de eventos.


## Responsabilidade de cada módulo

- **main.py**: orquestração da aplicação. Não contém regra de negócio do domínio de eventos, apenas instância o FastAPI e registra o router

- **app/models**: define o que a API aceita como entrada e o que ela expõe como saída, além da representação interna completa usada pelo armazenamento

- **app/database**: concentra toda a lógica de armazenamento e consulta de eventos

- **app/routes**: define os endpoints HTTP do recurso "evento"

## Como rodar

pip install -r requirements.txt
python -m uvicorn main:app --reload
