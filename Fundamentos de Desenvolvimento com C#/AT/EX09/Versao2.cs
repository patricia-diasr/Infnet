namespace EX09 {
    internal class Versao2 {
        private string caminhoArquivo = "estoque.txt";

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
            Console.Write("Digite o nome do produto: ");
            string nome = Console.ReadLine();

            Console.Write("Digite a quantidade em estoque: ");
            int quantidade = int.Parse(Console.ReadLine());

            Console.Write("Digite o preço unitário: ");
            double preco = double.Parse(Console.ReadLine());

            Produto produto = new Produto(nome, quantidade, preco);

            try {
                if (File.Exists(caminhoArquivo)) {
                    using (StreamWriter sw = File.AppendText(caminhoArquivo)) {
                        sw.WriteLine(produto.ToString());
                    }
                }
                else {
                    using (StreamWriter sw = new StreamWriter(caminhoArquivo)) {
                        sw.WriteLine(produto.ToString());
                    }
                }

                Console.WriteLine("Produto inserido com sucesso!");
            }
            catch (Exception ex) {
                Console.WriteLine($"Erro ao inserir produto: {ex.Message}");
            }
        }

        private void ListarProdutos() {
            try {
                if (File.Exists(caminhoArquivo) && new FileInfo(caminhoArquivo).Length > 0) {
                    using (StreamReader sr = new StreamReader(caminhoArquivo)) {
                        string linha;
                        while ((linha = sr.ReadLine()) != null) {
                            var produto = linha.Split(',');
                            Console.WriteLine($"Produto: {produto[0]} | Quantidade: {produto[1]} | Preço: R$ {produto[2]}");
                        }
                    }
                }
                else {
                    Console.WriteLine("Nenhum produto cadastrado.");
                }
            }
            catch (Exception ex) {
                Console.WriteLine($"Erro ao listar produtos: {ex.Message}");
            }
        }
    }
}
