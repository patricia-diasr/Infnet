package org.tasks.controller;

import io.javalin.Javalin;
import org.tasks.dto.EchoMessageDto;
import org.tasks.dto.TarefaDto;
import org.tasks.model.Tarefa;
import org.tasks.service.TarefaService;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class TarefaController {

    public static final String TAREFA_PATH = "/tarefas";
    public static final String TAREFA_BY_ID_PATH = TAREFA_PATH + "/{id}";

    private final TarefaService service;

    public TarefaController (TarefaService service) {
        this.service = service;
    }

    // Registra os endpoints REST no Javalin
    public void registrarRotas(Javalin app) {

        // Endpoint que retorna uma saudação
        app.get("/hello", ctx -> ctx.result("Hello, Javalin!"));

        // Endpoint que retorna status e timestamp atual
        app.get("/status", ctx -> {
            Map<String, Object> response = new HashMap<>();
            response.put("status", "ok");
            response.put("timestamp", Instant.now().toString());
            ctx.json(response);
        });

        // Endpoint que recebe mensagem e retorna a mesma mensagem
        app.post("/echo", ctx -> {
            EchoMessageDto message = ctx.bodyAsClass(EchoMessageDto.class);
            ctx.json(message);
        });

        // Endpoint que recebe um nome no path e retorna uma saudação personalizada
        app.get("/saudacao/{nome}", ctx -> {
            String nome = ctx.pathParam("nome");
            Map<String, String> response = new HashMap<>();
            response.put("mensagem", "Olá, " + nome + "!");
            ctx.json(response);
        });

        // Endpoint que retorna todas as tarefas cadastradas
        app.get(TAREFA_PATH, ctx -> ctx.json(service.listar()));

        // Endpoint que busca uma tarefa por ID e retorna em JSON
        app.get(TAREFA_BY_ID_PATH, ctx -> {
            UUID id = UUID.fromString(ctx.pathParam("id"));
            ctx.json(service.buscarPorId(id));
        });

        // Endpoint que cria uma nova tarefa a partir do JSON enviado
        app.post(TAREFA_PATH, ctx -> {
            TarefaDto dto = ctx.bodyValidator(TarefaDto.class)
                    .check(t -> t.getTitulo() != null && !t.getTitulo().isBlank(), "Título obrigatório!")
                    .get();

            Tarefa novaTarefa = service.salvar(dto);
            ctx.status(201).json(novaTarefa);
        });
    }
}
