package org.tasks.dto;

public class EchoMessageDto {
    public String mensagem;

    // Construtores

    public EchoMessageDto() {}

    public EchoMessageDto(String mensagem) {
        this.mensagem = mensagem;
    }

    // Getters e Setters

    public String getMensagem() {
        return mensagem;
    }

    public void setMensagem(String mensagem) {
        this.mensagem = mensagem;
    }
}
