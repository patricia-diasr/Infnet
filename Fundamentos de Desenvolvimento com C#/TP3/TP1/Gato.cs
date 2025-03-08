using System;

namespace TP1 {
    // Definição da classe Gato
    public class Gato {
        // Atributos (características do gato)
        private string nome;
        private int idade;

        // Construtor da classe (inicializa os atributos)
        public Gato(string nome, int idade) {
            this.nome = nome;
            this.idade = idade;
        }

        // Método que simula um som emitido pelo gato
        public void Miar() {
            Console.WriteLine(nome + " está miando!");
        }

        // Método para exibir informações sobre o gato
        public void ExibirDetalhes() {
            Console.WriteLine("Nome: " + nome);
            Console.WriteLine("Idade: " + idade + " anos");
        }
    }
}
