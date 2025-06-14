package org.tasks.client;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class TarefaClient {

    // Método principal que executa os testes dos endpoints na ordem
    public static void main(String[] args) throws IOException {
        String tarefaId = criarTarefa();
        listarTarefas();
        buscarTarefaPorId(tarefaId);
        verificarStatus();
    }

    // Envia requisição POST para criar uma nova tarefa e retorna o ID criado
    private static String criarTarefa() throws IOException {
        System.out.println("\nPOST /tarefas");

        URL url = new URL("http://localhost:7000/tarefas");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        String jsonInput = """
        {
            "titulo": "AT de Java",
            "descricao": "Fazer exercícios e organizar entrega",
            "prioridade": 2
        }""";

        System.out.println("Body: " + jsonInput);

        try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonInput.getBytes());
            os.flush();
        }

        int responseCode = conn.getResponseCode();
        System.out.println("Código de resposta: " + responseCode);

        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
        }

        conn.disconnect();

        String json = response.toString();
        String id = json.replaceAll(".*\"id\"\\s*:\\s*\"([^\"]+)\".*", "$1");

        return id;
    }

    // Envia requisição GET para listar todas as tarefas
    private static void listarTarefas() throws IOException {
        System.out.println("\nGET /tarefas");

        URL url = new URL("http://localhost:7000/tarefas");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int responseCode = conn.getResponseCode();
        System.out.println("Código de resposta: " + responseCode);

        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String line;
            System.out.println("Resposta:");

            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        }

        conn.disconnect();
    }

    // Envia requisição GET para buscar uma tarefa pelo ID informado
    private static void buscarTarefaPorId(String id) throws IOException {
        System.out.println("\nGET /tarefas/" + id);

        URL url = new URL("http://localhost:7000/tarefas/" + id);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int responseCode = conn.getResponseCode();
        System.out.println("Código de resposta: " + responseCode);

        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String line;
            System.out.println("Resposta:");

            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        }

        conn.disconnect();
    }

    // Envia requisição GET para consultar o status do servidor
    private static void verificarStatus() throws IOException {
        System.out.println("\nGET /status");

        URL url = new URL("http://localhost:7000/status");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int responseCode = conn.getResponseCode();
        System.out.println("Código de resposta: " + responseCode);

        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            String line;
            System.out.println("Resposta:");

            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        }

        conn.disconnect();
    }
}
