# ASSESSMENT

## ✅ Etapa 1: Desenvolvimento REST com Javalin

### Objetivos:
- Criar uma aplicação REST com endpoints básicos e um endpoint de cadastro.

### Funcionalidades:
- `GET /hello`: retorna `"Hello, Javalin!"`
- `GET /status`: retorna um JSON com status e timestamp no formato ISO-8601.
- `POST /echo`: retorna o mesmo JSON enviado com a chave `mensagem`.
- `GET /saudacao/{nome}`: retorna uma saudação personalizada.
- `POST /tarefas`: cadastra uma nova tarefa.
- `GET /tarefas`: retorna todas as tarefas cadastradas.
- `GET /tarefas/{id}`: retorna uma tarefa específica pelo ID.

### 📁 Arquivo:
> Implementação completa no arquivo  
[`org.tasks.controller.TarefaController.java`](src/main/java/org/tasks/controller/TarefaController.java)

### ▶️ Como rodar:
1. Execute o método `main` da classe  
   [`org.tasks.Main.java`](src/main/java/org/tasks/Main.java)
> Isso iniciará o servidor na porta **7000**

---

## 🧪 Etapa 2: Testes Unitários com JUnit

### Objetivos:
- Garantir que os principais endpoints estejam funcionando corretamente.

### Testes implementados:
- Teste para `GET /hello`
- Teste para `POST /tarefas`
- Teste para `GET /tarefas/{id}`
- Teste para `GET /tarefas`

### 📁 Arquivo:
> Todos os testes estão no arquivo  
[`org.tasks.controller.TarefaControllerTest.java`](src/test/java/org/tasks/controller/TarefaControllerTest.java)

### ▶️ Como rodar:
1. Execute os testes JUnit diretamente na classe `TarefaControllerTest`

---

## 🌐 Etapa 3: Consumo de API com HttpURLConnection

### Objetivos:
- Criar um cliente Java que consome os endpoints REST utilizando `HttpURLConnection`.

### Funcionalidades do cliente:
- Envia um `POST` para cadastrar uma nova tarefa.
- Realiza um `GET` para listar todas as tarefas.
- Realiza um `GET` com path param para buscar uma tarefa por ID.
- Faz um `GET /status` para verificar o status da aplicação.

### 📁 Arquivo:
> Implementação completa no arquivo  
[`org.tasks.client.TarefaClient.java`](src/main/java/org/tasks/client/TarefaClient.java)

### ▶️ Como rodar:
1. Execute o método `main` da classe  
   [`org.tasks.Main.java`](src/main/java/org/tasks/Main.java)
> (para subir a API)

2. Em seguida, execute o método `main` da classe  
   [`org.tasks.client.TarefaClient.java`](src/main/java/org/tasks/client/TarefaClient.java)
> (para executar o cliente e consumir a API)
