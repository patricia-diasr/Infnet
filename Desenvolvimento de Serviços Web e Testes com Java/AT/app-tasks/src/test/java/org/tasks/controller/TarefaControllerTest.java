package org.tasks.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import io.javalin.Javalin;
import io.javalin.testtools.JavalinTest;
import org.jetbrains.annotations.NotNull;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.Mock;

import org.tasks.dto.TarefaDto;
import org.tasks.model.Tarefa;
import org.tasks.service.TarefaService;

import java.time.temporal.ChronoUnit;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class TarefaControllerTest {

    @Mock
    private TarefaService tarefaService;

    @InjectMocks
    private TarefaController tarefaController;

    private ObjectMapper objectMapper;

    // Inicializa o ObjectMapper para lidar com LocalDateTime
    @BeforeEach
    void setup() {
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
    }

    // Cria uma instância do Javalin com as rotas do controller para testes
    @NotNull
    private Javalin criarAppComRotas() {
        Javalin app = Javalin.create();
        tarefaController.registrarRotas(app);
        return app;
    }

    // Testa endpoint GET /hello que retorna uma saudação simples
    @Test
    void deveRetornarHelloJavalin() {
        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            var response = client.get("/hello");
            assertEquals(200, response.code());
            assertEquals("Hello, Javalin!", response.body().string());
        });
    }

    // Testa endpoint GET /status que retorna status e timestamp
    @Test
    void deveRetornarStatusOkComTimestamp() {
        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            var response = client.get("/status");
            assertEquals(200, response.code());

            var json = objectMapper.readTree(response.body().string());
            assertEquals("ok", json.get("status").asText());
            assertNotNull(json.get("timestamp").asText());
        });
    }

    // Testa endpoint GET /saudacao/:nome que retorna mensagem personalizada
    @Test
    void deveRetornarSaudacaoComNome() {
        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            var response = client.get("/saudacao/Ana");
            assertEquals(200, response.code());

            var json = objectMapper.readTree(response.body().string());
            assertEquals("Olá, Ana!", json.get("mensagem").asText());
        });
    }

    // Testa buscar tarefa por ID, simulando retorno do serviço com mock
    @Test
    void deveRetornarTarefaPorId() throws Exception {
        UUID id = UUID.randomUUID();
        Tarefa tarefa = new Tarefa();
        tarefa.setId(id);
        tarefa.setTitulo("Tarefa Teste");
        tarefa.setPrioridade(1);

        when(tarefaService.buscarPorId(id)).thenReturn(tarefa);

        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            var response = client.get("/tarefas/" + id);
            assertEquals(200, response.code());

            var tarefaRetornada = objectMapper.readValue(response.body().string(), Tarefa.class);
            assertEquals("Tarefa Teste", tarefaRetornada.getTitulo());
            assertEquals(id, tarefaRetornada.getId());
        });
    }

    // Testa criação de nova tarefa via POST, validando resposta e dados retornados
    @Test
    void deveCriarNovaTarefaComSucesso() {
        TarefaDto dto = new TarefaDto();
        dto.setTitulo("Nova tarefa de teste");
        dto.setDescricao("Descrição da tarefa");
        dto.setPrioridade(1);

        var tarefaSalva = new Tarefa("Nova tarefa de teste", "Descrição da tarefa", false, 1);

        when(tarefaService.salvar(any())).thenReturn(tarefaSalva);

        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            String jsonBody = objectMapper.writeValueAsString(dto);
            var response = client.post("/tarefas", jsonBody);

            assertEquals(201, response.code());

            Tarefa responseTarefa = objectMapper.readValue(response.body().string(), Tarefa.class);

            // Comparação do conteúdo esperado e o que foi retornado
            assertEquals(tarefaSalva.getId(), responseTarefa.getId());
            assertEquals(tarefaSalva.getTitulo(), responseTarefa.getTitulo());
            assertEquals(tarefaSalva.getConcluido(), responseTarefa.getConcluido());
            assertEquals(
                    tarefaSalva.getDataCriacao().truncatedTo(ChronoUnit.SECONDS),
                    responseTarefa.getDataCriacao().truncatedTo(ChronoUnit.SECONDS)
            );
        });

        verify(tarefaService).salvar(any(TarefaDto.class));
    }

    // Testa validação: não permite criar tarefa com título vazio, deve retornar 400
    @Test
    void naoDeveCriarTarefaComTituloVazio() throws Exception {
        JavalinTest.test(criarAppComRotas(), (server, client) -> {
            TarefaDto dto = new TarefaDto();
            dto.setTitulo("");
            dto.setDescricao("Descrição");
            dto.setPrioridade(2);

            String json = objectMapper.writeValueAsString(dto);

            var response = client.post("/tarefas", json);

            assertEquals(400, response.code());
            String responseBody = response.body().string();
            assertTrue(responseBody.contains("Título obrigatório!"));
        });
    }

}
