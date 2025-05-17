package org.clinica.domain;

import java.util.List;

// Histórico de consultas realizadas.
public interface HistoricoConsultas {

    // Salva uma nova consulta no histórico.
    void salvarConsulta(Consulta consulta);

    // Retorna a lista de consultas realizadas por um paciente específico.
    List<Consulta> consultasPorPaciente(Paciente paciente);
}