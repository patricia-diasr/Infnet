package org.tasks;

import io.javalin.Javalin;
import org.jetbrains.annotations.NotNull;
import org.tasks.config.DbConfig;
import org.tasks.controller.TarefaController;
import org.tasks.repository.TarefaRepository;
import org.tasks.service.TarefaService;

public class Main {
    // Método principal que inicia o servidor e registra as rotas
    public static void main(String[] args) {
        Javalin app = Javalin.create().start(7000);
        var tarefaService = inicializacaoDosObjetos();

        new TarefaController(tarefaService).registrarRotas(app);
    }

    // Inicializa os objetos necessários para a aplicação
    @NotNull
    private static TarefaService inicializacaoDosObjetos() {
        var dbConfig = DbConfig.createJdbi();
        var tarefaRepository = new TarefaRepository(dbConfig);

        return new TarefaService(tarefaRepository);
    }
}
