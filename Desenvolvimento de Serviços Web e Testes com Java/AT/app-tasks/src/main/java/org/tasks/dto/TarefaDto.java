package org.tasks.dto;

import java.time.LocalDateTime;

public class TarefaDto {

    private String titulo;
    private String descricao;
    private boolean concluido;
    private int prioridade;

    // Construtores

    public TarefaDto() {
    }

    public TarefaDto(String titulo, String descricao, Boolean concluido, int prioridade) {
        this.titulo = titulo;
        this.descricao = descricao;
        this.concluido = concluido;
        this.prioridade = prioridade;
    }

    // Getters e Setters

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

    public int getPrioridade() {
        return prioridade;
    }

    public void setPrioridade(int prioridade) {
        this.prioridade = prioridade;
    }
}
