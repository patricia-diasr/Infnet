package org.tasks.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.tasks.dto.TarefaDto;
import org.tasks.model.Tarefa;
import org.tasks.repository.TarefaRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class TarefaServiceTest {

    private TarefaRepository repository;
    private TarefaService service;

    // Configura o mock do repositório e instancia o serviço antes de cada teste
    @BeforeEach
    void setUp() {
        repository = Mockito.mock(TarefaRepository.class);
        service = new TarefaService(repository);
    }

    // Testa se o método listar() retorna todas as tarefas corretamente
    @Test
    void deveListarTodasAsTarefas() {
        List<Tarefa> tarefas = List.of(new Tarefa(), new Tarefa());
        when(repository.findAll()).thenReturn(tarefas);

        List<Tarefa> resultado = service.listar();

        assertEquals(2, resultado.size());
        verify(repository).findAll();
    }

    // Testa se buscarPorId() retorna a tarefa correta quando ela existe
    @Test
    void deveBuscarTarefaPorIdExistente() {
        UUID id = UUID.randomUUID();
        Tarefa tarefa = new Tarefa();
        tarefa.setId(id);
        when(repository.findById(id)).thenReturn(Optional.of(tarefa));

        Tarefa resultado = service.buscarPorId(id);

        assertNotNull(resultado);
        assertEquals(id, resultado.getId());
        verify(repository).findById(id);
    }

    // Testa se buscarPorId() lança exceção quando a tarefa não existe
    @Test
    void deveLancarExcecaoQuandoTarefaNaoExistir() {
        UUID id = UUID.randomUUID();
        when(repository.findById(id)).thenReturn(Optional.empty());

        assertThrows(io.javalin.http.NotFoundResponse.class, () -> service.buscarPorId(id));
        verify(repository).findById(id);
    }

    // Testa se salvar() cria uma nova tarefa e retorna o objeto salvo corretamente
    @Test
    void deveSalvarNovaTarefaComSucesso() {
        TarefaDto dto = new TarefaDto();
        dto.setTitulo("Nova tarefa");
        dto.setDescricao("Descrição");
        dto.setConcluido(false);
        dto.setPrioridade(1);

        UUID idGerado = UUID.randomUUID();
        Tarefa tarefaCriada = new Tarefa();
        tarefaCriada.setId(idGerado);

        when(repository.insert(any(Tarefa.class))).thenReturn(idGerado);
        when(repository.findById(idGerado)).thenReturn(Optional.of(tarefaCriada));

        Tarefa resultado = service.salvar(dto);

        assertNotNull(resultado);
        assertEquals(idGerado, resultado.getId());

        verify(repository).insert(any(Tarefa.class));
        verify(repository).findById(idGerado);
    }
}
