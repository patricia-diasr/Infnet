package org.clinica.domain;

// Auditoria responsável por registrar consultas
public interface Auditoria {

    // Registra uma consulta no sistema de auditoria.
    void registrarConsulta(Consulta consulta);
}