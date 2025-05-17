package org.clinica.domain;

// Define a regra para autorização de reembolso de consultas.
public interface AutorizadorReembolso {

    // Verifica se o reembolso para uma determinada consulta está autorizado.
    boolean isAutorizado(Paciente paciente, Consulta consulta);
}
