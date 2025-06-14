CREATE TABLE tarefas (
    id UUID PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    concluido BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP NOT NULL,
    prioridade INT
);
