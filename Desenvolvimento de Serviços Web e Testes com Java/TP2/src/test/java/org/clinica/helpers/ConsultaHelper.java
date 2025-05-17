package org.clinica.helpers;

import org.clinica.domain.Consulta;
import org.clinica.domain.Paciente;

import java.time.LocalDate;
import java.time.LocalDateTime;

// Helper para criar objetos Consulta prontos para uso em testes.
public class ConsultaHelper {

    private static final String NOME_PADRAO = "Maria Silva";
    private static final String CPF_PADRAO = "123.456.789-00";
    private static final LocalDate DATA_NASCIMENTO_PADRAO = LocalDate.of(1990, 2, 1);

    // Cria uma consulta padrão com valor fixo (200.0).
    public static Consulta criarConsultaPadrao() {
        return criarConsultaComValor(200.0);
    }

    // Cria uma consulta com valor específico.
    public static Consulta criarConsultaComValor(double valor) {
        Paciente pacienteDummy = new Paciente(
                NOME_PADRAO,
                DATA_NASCIMENTO_PADRAO,
                CPF_PADRAO
        );
        return new Consulta(pacienteDummy, LocalDateTime.now(), valor);
    }
}
