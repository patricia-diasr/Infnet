package org.tasks.model;

import com.fasterxml.jackson.annotation.JsonFormat;

import java.time.LocalDateTime;
import java.util.UUID;

public class Tarefa {

    private UUID id;
    private String titulo;
    private String descricao;
    private boolean concluido = false;
    private int prioridade;

    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime dataCriacao;

    // Construtores

    public Tarefa() {
        this.id = UUID.randomUUID();
        this.dataCriacao = LocalDateTime.now();
    }

    public Tarefa(String titulo, String descricao, Boolean concluido, int prioridade) {
        this();
        this.titulo = titulo;
        this.descricao = descricao;
        this.concluido = concluido;
        this.prioridade = prioridade;
    }

    // Getters e setters

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public boolean getConcluido() {
        return concluido;
    }

    public void setConcluido(boolean concluido) {
        this.concluido = concluido;
    }

    public LocalDateTime getDataCriacao() {
        return dataCriacao;
    }

    public void setDataCriacao(LocalDateTime dataCriacao) {
        this.dataCriacao = dataCriacao;
    }

    public int getPrioridade() {
        return prioridade;
    }

    public void setPrioridade(int prioridade) {
        this.prioridade = prioridade;
    }
}
