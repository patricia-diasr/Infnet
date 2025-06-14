package org.tasks.config;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.jdbi.v3.core.Jdbi;

import javax.sql.DataSource;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.SQLException;

public class DbConfig {

    // Cria e configura o Jdbi com conexão ao banco e executa script SQL inicial
    public static Jdbi createJdbi() {
        var ds = createDataSource();

        try (Connection conn = ds.getConnection()) {
            runScript(conn, "tasks.sql");
        } catch (SQLException | IOException e) {
            throw new RuntimeException(e);
        }

        return Jdbi.create(ds);
    }

    // Executa o script SQL passado como arquivo na conexão fornecida
    private static void runScript(Connection conn, String s) throws IOException {
        var input = DbConfig.class.getClassLoader().getResourceAsStream(s);

        if (input == null) {
            throw new IOException("Arquivo não encontrado!");
        }

        var sql = new String(input.readAllBytes(), StandardCharsets.UTF_8);

        try (var stmt = conn.createStatement()) {
            stmt.execute(sql);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    // Configura e retorna um DataSource HikariCP para conexão com banco H2 em memória
    private static DataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1");
        config.setUsername("sa");
        config.setPassword("");
        return new HikariDataSource(config);
    }
}
