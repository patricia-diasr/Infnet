package org.clinica.domain;

import java.time.LocalDate;
import java.util.Objects;

// Paciente da clínica que realiza as consultas
public class Paciente {

    private String nome;              // Nome completo do paciente
    private LocalDate dataNascimento; // Data de nascimento do paciente
    private String cpf;               // CPF do paciente

    // Constructor
    public Paciente(String nome, LocalDate dataNascimento, String cpf) {
        setNome(nome);
        setDataNascimento(dataNascimento);
        setCpf(cpf);
    }

    // Getters e Setters
    public String getNome() {
        return nome;
    }

    public LocalDate getDataNascimento() {
        return dataNascimento;
    }

    public String getCpf() {
        return cpf;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setDataNascimento(LocalDate dataNascimento) {
        this.dataNascimento = dataNascimento;
    }

    public void setCpf(String cpf) {
        this.cpf = cpf;
    }
}
