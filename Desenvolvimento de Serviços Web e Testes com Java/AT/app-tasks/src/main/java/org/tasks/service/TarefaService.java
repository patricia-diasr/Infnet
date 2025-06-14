package org.tasks.service;

import io.javalin.http.NotFoundResponse;
import org.tasks.dto.TarefaDto;
import org.tasks.model.Tarefa;
import org.tasks.repository.TarefaRepository;

import java.util.List;
import java.util.UUID;

public class TarefaService {
    private final TarefaRepository repository;

    public TarefaService (TarefaRepository repository) {
        this.repository = repository;
    }

    // Retorna a lista de todas as tarefas
    public List<Tarefa> listar() {
        return repository.findAll();
    }

    // Busca uma tarefa pelo ID, lança erro 404 se não encontrada
    public Tarefa buscarPorId(UUID id) {
        return repository.findById(id)
                .orElseThrow(() -> new NotFoundResponse("Tarefa Não encontrada!"));
    }

    // Salva uma nova tarefa a partir do DTO e retorna o objeto salvo completo
    public Tarefa salvar(TarefaDto dto) {
        Tarefa tarefa = construirTarefaAPartirDoDTO(dto);
        UUID id = repository.insert(tarefa);

        return buscarPorId(id);
    }

    // Constrói um objeto Tarefa a partir dos dados do DTO
    private Tarefa construirTarefaAPartirDoDTO(TarefaDto dto) {
        Tarefa tarefa = new Tarefa();

        tarefa.setTitulo(dto.getTitulo());
        tarefa.setDescricao(dto.getDescricao());
        tarefa.setConcluido(dto.getConcluido());
        tarefa.setPrioridade(dto.getPrioridade());

        return tarefa;
    }
}
