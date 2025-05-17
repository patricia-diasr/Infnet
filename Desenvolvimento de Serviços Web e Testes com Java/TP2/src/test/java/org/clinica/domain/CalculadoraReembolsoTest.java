package org.clinica.domain;

import org.clinica.helpers.AssertHelper;
import org.clinica.helpers.ConsultaHelper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.clinica.stubs.PlanoSaudeStubs.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

// Testes unitários para a classe CalculadoraReembolso.
public class CalculadoraReembolsoTest {

    private AutorizadorReembolso autorizadorMock;
    private CalculadoraReembolso calculadora;
    private Paciente pacienteDummy;

    @BeforeEach
    public void setup() {
        autorizadorMock = mock(AutorizadorReembolso.class);
        when(autorizadorMock.isAutorizado(any(Paciente.class), any(Consulta.class))).thenReturn(true);
        calculadora = new CalculadoraReembolso(autorizadorMock);
        pacienteDummy = new Paciente("Maria Silva", LocalDate.of(1990, 2, 1), "123.456.789-00");
    }

    @Test
    public void deveCalcularReembolsoComBaseNoValorEPercentual() {
        PlanoSaude plano = PlanoSetenta;
        Consulta consulta = ConsultaHelper.criarConsultaPadrao();

        double reembolso = calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        AssertHelper.assertAproximadamenteIgual(140.0, reembolso);
    }

    @Test
    public void deveCalcularReembolsoComValorConsultaZero() {
        PlanoSaude plano = PlanoOitenta;
        Consulta consulta = ConsultaHelper.criarConsultaComValor(0.0);

        double reembolso = calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        AssertHelper.assertAproximadamenteIgual(0.0, reembolso);
    }

    @Test
    public void deveCalcularReembolsoComValorConsultaCem() {
        PlanoSaude plano = PlanoOitenta;
        Consulta consulta = ConsultaHelper.criarConsultaComValor(100.0);

        double reembolso = calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        AssertHelper.assertAproximadamenteIgual(80.0, reembolso);
    }

    @Test
    public void deveCalcularReembolsoComCoberturaZero() {
        PlanoSaude plano = PlanoZero;
        Consulta consulta = ConsultaHelper.criarConsultaPadrao();

        double reembolso = calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        AssertHelper.assertAproximadamenteIgual(0.0, reembolso);
    }

    @Test
    public void deveCalcularReembolsoComCoberturaCem() {
        PlanoSaude plano = PlanoCem;
        Consulta consulta = ConsultaHelper.criarConsultaComValor(100.0);

        double reembolso = calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        AssertHelper.assertAproximadamenteIgual(100.0, reembolso);
    }

    @Test
    public void deveLancarExcecaoQuandoNaoAutorizado() {
        PlanoSaude plano = PlanoOitenta;
        Consulta consulta = ConsultaHelper.criarConsultaPadrao();

        when(autorizadorMock.isAutorizado(any(Paciente.class), any(Consulta.class))).thenReturn(false);
        IllegalStateException excecao = assertThrows(IllegalStateException.class, () -> {
            calculadora.calcularReembolso(pacienteDummy, plano, consulta);
        });

        assertEquals("Consulta não autorizada para reembolso.", excecao.getMessage());
        verify(autorizadorMock, times(1)).isAutorizado(pacienteDummy, consulta);
    }

    @Test
    public void deveAplicarTetoDeReembolsoQuandoUltrapassa150() {
        PlanoSaude plano = PlanoNoventa;
        Consulta consulta = ConsultaHelper.criarConsultaComValor(200.0);

        double reembolso = calculadora.calcularReembolso(consulta.getPaciente(), plano, consulta);
        AssertHelper.assertAproximadamenteIgual(150.0, reembolso);
    }

    @Test
    public void devePermitirReembolsoAbaixoDoTeto() {
        PlanoSaude plano = PlanoSessenta;
        Consulta consulta = ConsultaHelper.criarConsultaComValor(200.0);

        double reembolso = calculadora.calcularReembolso(consulta.getPaciente(), plano, consulta);
        AssertHelper.assertAproximadamenteIgual(120.0, reembolso);
    }
}
