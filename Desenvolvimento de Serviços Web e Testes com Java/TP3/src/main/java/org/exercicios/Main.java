package org.exercicios;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class Main {
    public static void main(String[] args) {
        System.out.println("=== Exercício 1 ===");
        getAllEntities();

        System.out.println("\n=== Exercício 2 ===");
        getEntityById(5);

        System.out.println("\n=== Exercício 3 ===");
        getEntityByIdWithNotFoundCheck(13);

        System.out.println("\n=== Exercício 4 ===");
        getEntitiesWithParams("teste", 5);

        System.out.println("\n=== Exercício 5 ===");
        createEntity();

        System.out.println("\n=== Exercício 6 ===");
        createAndGetEntity();

        System.out.println("\n=== Exercício 7 ===");
        updateEntityWithPost(10, "atualizado");

        System.out.println("\n=== Exercício 8 ===");
        updateEntityWithPut(10, "atualizado");

        System.out.println("\n=== Exercício 9 ===");
        deleteEntity(9);

        System.out.println("\n=== Exercício 10 ===");
        deleteInvalidEntity(2);

        System.out.println("\n=== Exercício 11 ===");
        optionsEntities();

        System.out.println("\n=== Exercício 12 ===");
        System.out.println("a)");
        getAllItems();

        System.out.println("\nb)");
        String isbn = getRandomISBN();

        System.out.println("\nc)");
        createItem(isbn, "book", 29.80, 12);

        System.out.println("\nd)");
        String isbn2 = getRandomISBN();
        updateItem(12, isbn2, "book", 30.80, 11);

        System.out.println("\ne)");
        deleteItem(12);
    }

    // Exercício 1
    public static void getAllEntities() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 2
    public static void getEntityById(int id) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("ID da Entidade: " + id);
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 3
    public static void getEntityByIdWithNotFoundCheck(int id) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("ID da Entidade: " + id);
            System.out.println("Código de Status HTTP: " + statusCode);

            if (statusCode == 200) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder resposta = new StringBuilder();

                while ((inputLine = in.readLine()) != null) {
                    resposta.append(inputLine);
                }
                in.close();

                System.out.println("Resposta da requisição:");
                System.out.println(resposta.toString());
            } else if (statusCode == 404) {
                System.out.println("Entidade com ID " + id + " não encontrada.");
            } else {
                System.out.println("Erro inesperado. Código de status: " + statusCode);
            }

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 4
    public static void getEntitiesWithParams(String categoria, int limite) {
        try {
            String urlString = String.format("https://apichallenges.eviltester.com/sim/entities?categoria=%s&limite=%d",
                    categoria, limite);
            URL url = new URL(urlString);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("URL final: " + urlString);
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 5
    public static void createEntity() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String jsonInput = "{\"name\": \"aluno\"}";

            connection.getOutputStream().write(jsonInput.getBytes());

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            if (statusCode == 200 || statusCode == 201) {
                String response = resposta.toString();
                int idStart = response.indexOf("\"id\":") + 5;
                int idEnd = response.indexOf(",", idStart);
                String id = response.substring(idStart, idEnd).trim();
                System.out.println("ID gerado: " + id);
            }

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 6
    public static void createAndGetEntity() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String jsonInput = "{\"name\": \"aluno\"}";

            connection.getOutputStream().write(jsonInput.getBytes());

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            if (statusCode == 200 || statusCode == 201) {
                String response = resposta.toString();
                int idStart = response.indexOf("\"id\":") + 5;
                int idEnd = response.indexOf(",", idStart);
                String id = response.substring(idStart, idEnd).trim();
                System.out.println("ID gerado: " + id);

                System.out.println("\nVerificando entidade criada:");
                getEntityById(Integer.parseInt(id));
            }

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 7
    public static void updateEntityWithPost(int id, String novoNome) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String jsonInput = String.format("{\"name\": \"%s\"}", novoNome);
            connection.getOutputStream().write(jsonInput.getBytes());

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

            System.out.println("\nVerificando entidade atualizada:");
            getEntityById(id);

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 8
    public static void updateEntityWithPut(int id, String novoNome) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("PUT");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String jsonInput = String.format("{\"name\": \"%s\"}", novoNome);
            connection.getOutputStream().write(jsonInput.getBytes());

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

            System.out.println("\nVerificando entidade atualizada:");
            getEntityById(id);

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 9
    public static void deleteEntity(int id) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("DELETE");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in;
            if (statusCode >= 200 && statusCode < 300) {
                in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
            }

            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

            System.out.println("\nVerificando entidade removida:");
            getEntityByIdWithNotFoundCheck(id);

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 10
    public static void deleteInvalidEntity(int id) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("DELETE");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in;
            if (statusCode >= 200 && statusCode < 300) {
                in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
            }

            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 11
    public static void optionsEntities() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/sim/entities");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("OPTIONS");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            String allowMethods = connection.getHeaderField("Allow");
            System.out.println("Métodos HTTP permitidos (Allow): " + allowMethods);

            connection.disconnect();

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 12.a
    public static void getAllItems() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/simpleapi/items");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 12.b
    public static String getRandomISBN() {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/simpleapi/randomisbn");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("GET");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String isbn = in.readLine();
            in.close();

            System.out.println("ISBN gerado: " + isbn);

            connection.disconnect();

            return isbn;
        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 12.c
    public static void createItem(String isbn, String type, Double price, int numberInStock) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/simpleapi/items");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String json = String.format(
                    Locale.US,
                    "{\"type\":\"%s\",\"isbn13\":\"%s\",\"price\":%.2f,\"numberinstock\":%d}",
                    type, isbn, price, numberInStock
            );

            try (OutputStream out = connection.getOutputStream()) {
                byte[] input = json.getBytes(StandardCharsets.UTF_8);
                out.write(input);
                out.flush();
            }

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(
                    statusCode >= 200 && statusCode < 300 ? connection.getInputStream() : connection.getErrorStream()
            ));

            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 12.d
    public static void updateItem(int id, String isbn, String type, Double price, int numberInStock) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/simpleapi/items/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("PUT");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String json = String.format(
                    Locale.US,
                    "{\"type\":\"%s\",\"isbn13\":\"%s\",\"price\":%.2f,\"numberinstock\":%d}",
                    type, isbn, price, numberInStock
            );

            try (OutputStream out = connection.getOutputStream()) {
                byte[] input = json.getBytes(StandardCharsets.UTF_8);
                out.write(input);
                out.flush();
            }

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in;
            if (statusCode >= 200 && statusCode < 300) {
                in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
            }

            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    // Exercício 12.e
    public static void deleteItem(int id) {
        try {
            URL url = new URL("https://apichallenges.eviltester.com/simpleapi/items/" + id);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("DELETE");

            int statusCode = connection.getResponseCode();
            System.out.println("Código de Status HTTP: " + statusCode);

            BufferedReader in;
            if (statusCode >= 200 && statusCode < 300) {
                in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            } else {
                in = new BufferedReader(new InputStreamReader(connection.getErrorStream()));
            }

            String inputLine;
            StringBuilder resposta = new StringBuilder();

            while ((inputLine = in.readLine()) != null) {
                resposta.append(inputLine);
            }
            in.close();

            System.out.println("Resposta da requisição:");
            System.out.println(resposta.toString());

            connection.disconnect();

        } catch (IOException e) {
            System.out.println("Erro: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }
}