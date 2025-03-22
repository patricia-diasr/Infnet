namespace EX09 {
    internal class Versao1 {
        private Produto[] produtos = new Produto[5];
        private int contador = 0;

        public void Menu() {
            while (true) {
                Console.Clear();
                Console.WriteLine("Menu de Opções:");
                Console.WriteLine("1. Inserir Produto");
                Console.WriteLine("2. Listar Produtos");
                Console.WriteLine("3. Sair");
                Console.Write("Escolha uma opção: ");
                string opcao = Console.ReadLine();

                switch (opcao) {
                    case "1":
                        InserirProduto();
                        break;

                    case "2":
                        ListarProdutos();
                        break;

                    case "3":
                        return;

                    default:
                        Console.WriteLine("Opção inválida! Tente novamente.");
                        break;
                }

                Console.WriteLine("\nPressione qualquer tecla para continuar...");
                Console.ReadKey();
            }
        }

        private void InserirProduto() {
            if (contador < 5) {
                Console.Write("Digite o nome do produto: ");
                string nome = Console.ReadLine();

                Console.Write("Digite a quantidade em estoque: ");
                int quantidade = int.Parse(Console.ReadLine());

                Console.Write("Digite o preço unitário: ");
                double preco = double.Parse(Console.ReadLine());

                produtos[contador] = new Produto(nome, quantidade, preco);
                contador++;

                Console.WriteLine("Produto inserido com sucesso!");
            }
            else {
                Console.WriteLine("Limite de produtos atingido!");
            }
        }

        private void ListarProdutos() {
            if (contador == 0) {
                Console.WriteLine("Nenhum produto cadastrado.");
            }
            else {
                for (int i = 0; i < contador; i++) {
                    var produto = produtos[i];
                    Console.WriteLine($"Produto: {produto.Nome} | Quantidade: {produto.Quantidade} | Preço: R$ {produto.Preco:F2}");
                }
            }
        }
    }
}
