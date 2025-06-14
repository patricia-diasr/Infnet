package org.tasks.repository;

import org.jdbi.v3.core.Jdbi;
import org.tasks.model.Tarefa;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public class TarefaRepository {
    private final Jdbi jdbi;

    // Construtor que recebe a instância do Jdbi para conexão com o banco
    public TarefaRepository(Jdbi jdbi) {
        this.jdbi = jdbi;
    }

    // Busca todas as tarefas no banco
    public List<Tarefa> findAll() {
        return jdbi.withHandle(handle -> handle.createQuery("SELECT * FROM tarefas")
                .mapToBean(Tarefa.class)
                .list());
    }

    // Busca uma tarefa pelo ID, retornando Optional
    public Optional<Tarefa> findById(UUID id) {
        return jdbi.withHandle(handle ->
                handle.createQuery("SELECT * FROM tarefas WHERE id = :id")
                        .bind("id", id)
                        .mapToBean(Tarefa.class)
                        .findOne());
    }

    // Insere uma nova tarefa no banco e retorna o ID gerado
    public UUID insert(Tarefa t) {
        return jdbi.withHandle(handle ->
                handle.createUpdate("INSERT INTO tarefas (id, titulo, descricao, concluido, data_criacao, prioridade) " +
                                "VALUES (:id, :titulo, :descricao, :concluido, :dataCriacao, :prioridade)")
                        .bindBean(t)
                        .executeAndReturnGeneratedKeys("id")
                        .mapTo(UUID.class)
                        .one());
    }
}
