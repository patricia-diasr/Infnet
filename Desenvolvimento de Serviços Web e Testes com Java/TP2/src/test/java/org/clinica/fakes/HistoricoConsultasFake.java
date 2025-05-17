package org.clinica.fakes;

import org.clinica.domain.Auditoria;
import org.clinica.domain.Consulta;
import org.clinica.domain.HistoricoConsultas;
import org.clinica.domain.Paciente;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

// Fake de HistoricoConsultas para uso em testes.
// Armazena consultas em memória e registra auditoria quando salvar.
public class HistoricoConsultasFake implements HistoricoConsultas {

    private Auditoria auditoria;
    private final List<Consulta> consultas = new ArrayList<>();

    public void setAuditoria(Auditoria auditoria) {
        this.auditoria = auditoria;
    }

    // Salva a consulta no histórico e registra auditoria.
    @Override
    public void salvarConsulta(Consulta consulta) {
        if (auditoria == null) {
            throw new IllegalStateException("Auditoria não configurada");
        }
        auditoria.registrarConsulta(consulta);
        consultas.add(consulta);
    }

    // Retorna lista de consultas para um paciente específico.
    @Override
    public List<Consulta> consultasPorPaciente(Paciente paciente) {
        return consultas.stream()
                .filter(c -> Objects.equals(c.getPaciente(), paciente))
                .collect(Collectors.toList());
    }
}
