package org.clinica.domain;

// Calcular o valor do reembolso de uma consulta, verificando autorização
// e aplicando regras de cobertura e teto máximo.
public class CalculadoraReembolso {

    private AutorizadorReembolso autorizador;
    final double VALOR_TETO = 150.0;

    // Construtor que recebe o autorizador de reembolso a ser usado.
    public CalculadoraReembolso(AutorizadorReembolso autorizador) {
        if (autorizador == null) {
            throw new IllegalArgumentException("Autorizador não pode ser nulo.");
        }
        this.autorizador = autorizador;
    }

    // Calcula o valor do reembolso para uma consulta.
    public double calcularReembolso(Paciente paciente, PlanoSaude planoSaude, Consulta consulta) {
        if (!autorizador.isAutorizado(paciente, consulta)) {
            throw new IllegalStateException("Consulta não autorizada para reembolso.");
        }

        double percentualCobertura = planoSaude.getPercentualCobertura();
        double valorConsulta = consulta.getValor();

        double valorReembolso = valorConsulta * (percentualCobertura / 100.0);
        return Math.min(valorReembolso, VALOR_TETO);
    }
}
