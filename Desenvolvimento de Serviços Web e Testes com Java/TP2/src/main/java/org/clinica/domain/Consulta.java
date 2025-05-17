package org.clinica.domain;

import java.time.LocalDate;
import java.time.LocalDateTime;

// Consulta realizada por um paciente
public class Consulta {

    private Paciente paciente; // Paciente que realizou a consulta
    private LocalDateTime data;    // Data da consulta
    private double valor;      // Valor cobrado pela consulta


    // Construtor
    public Consulta(Paciente paciente, LocalDateTime data, double valor) {
        this.paciente = paciente;
        this.data = data;
        this.valor = valor;
    }

    // Getters e Setters
    public Paciente getPaciente() {
        return paciente;
    }

    public LocalDateTime getData() {
        return data;
    }

    public double getValor() {
        return valor;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }

    public void setData(LocalDateTime data) {
        this.data = data;
    }

    public void setValor(double valor) {
        this.valor = valor;
    }
}
