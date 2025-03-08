using System;

namespace Show {
    public class Ingresso {
        // Nome do show para identificação no sistema
        public string NomeDoShow { get; set; }
        // Preço unitário do ingresso, essencial para cálculos financeiros e vendas
        public double Preco { get; set; }
        // Quantidade disponível de ingressos
        public int QuantidadeDisponivel { get; set; }

        // Construtor para inicializar todos os atributos
        // O construtor facilita a criação do objeto, permitindo inicializar todos os atributos de uma vez
        public Ingresso(string nomeDoShow, double preco, int quantidadeDisponivel) {
            NomeDoShow = nomeDoShow;
            Preco = preco;
            QuantidadeDisponivel = quantidadeDisponivel;
        }

        // Método para alterar o preço do ingresso
        public void AlterarPreco(double novoPreco) {
            Preco = novoPreco;
            Console.WriteLine($"Preço alterado para R$ {Preco:F2}");
        }

        // Método para alterar a quantidade disponível de ingressos
        public void AlterarQuantidade(int novaQuantidade) {
            QuantidadeDisponivel = novaQuantidade;
            Console.WriteLine($"Quantidade de ingressos atualizada para {QuantidadeDisponivel}");
        }

        // Método para exibir as informações do ingresso
        public void ExibirInformacoes() {
            Console.WriteLine($"Show: {NomeDoShow}");
            Console.WriteLine($"Preço: R$ {Preco:F2}");
            Console.WriteLine($"Quantidade disponível: {QuantidadeDisponivel}");
        }
    }
}