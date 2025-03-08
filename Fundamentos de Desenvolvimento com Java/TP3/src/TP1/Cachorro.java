package TP1;

// Definição da classe Cachorro
public class Cachorro {
    // Atributos (características do cachorro)
    private String nome;
    private int idade;

    // Construtor da classe (inicializa os atributos)
    public Cachorro(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }

    // Método que simula um som emitido pelo cachorro
    public void latir() {
        System.out.println(nome + " está latindo!");
    }

    // Método para exibir informações sobre o cachorro
    public void exibirDetalhes() {
        System.out.println("Nome: " + nome );
        System.out.println("Idade: " + idade + " anos");
    }
}
