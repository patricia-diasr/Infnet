package org.clinica.fakes;

import org.clinica.domain.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

// Testes unitários para a classe HistoricoConsultasFake.
public class HistoricoConsultasFakeTest {

    private HistoricoConsultasFake historico;
    private Auditoria auditoriaMock;

    private Paciente paciente;

    @BeforeEach
    public void setup() {
        auditoriaMock = mock(Auditoria.class);
        historico = new HistoricoConsultasFake();
        historico.setAuditoria(auditoriaMock);

        paciente = new Paciente("João Silva", LocalDate.of(1980, 1, 1), "111.222.333-44");
    }

    @Test
    public void deveSalvarEListarConsultasPorPaciente() {
        Consulta consulta = new Consulta(paciente, LocalDateTime.now(), 200.0);
        historico.salvarConsulta(consulta);

        List<Consulta> consultasPaciente = historico.consultasPorPaciente(paciente);

        assertEquals(1, consultasPaciente.size(), "Deve retornar 1 consulta para o paciente");
        assertTrue(consultasPaciente.contains(consulta), "Consulta salva deve estar na lista");
    }

    @Test
    public void deveRetornarListaVaziaSePacienteNaoTemConsultas() {
        Paciente outroPaciente = new Paciente("Maria", LocalDate.of(1990, 5, 10), "555.666.777-88");

        List<Consulta> consultas = historico.consultasPorPaciente(outroPaciente);

        assertTrue(consultas.isEmpty(), "Deve retornar lista vazia para paciente sem consultas");
    }

    @Test
    public void deveChamarAuditoriaAoSalvarConsulta() {
        Consulta consulta = new Consulta(paciente, LocalDateTime.now(), 100.0);
        historico.salvarConsulta(consulta);

        verify(auditoriaMock, times(1)).registrarConsulta(consulta);
    }
}
