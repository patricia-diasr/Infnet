namespace EX11 {
    internal class Program {
        private static string caminhoArquivo = "contatos.txt";
        static void Main(string[] args) {
            while (true) {
                Console.Clear();
                Console.WriteLine("=== Gerenciador de Contatos ===");
                Console.WriteLine("1. Adicionar novo contato");
                Console.WriteLine("2. Listar contatos cadastrados");
                Console.WriteLine("3. Sair");

                Console.Write("Escolha uma opção: ");
                string opcao = Console.ReadLine();

                switch (opcao) {
                    case "1":
                        InserirContato();
                        break;

                    case "2":
                        ListarContatos();
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

        private static void InserirContato() {
            Console.WriteLine("\nAdicionando novo contato...");
            Console.Write("Nome: ");
            string nome = Console.ReadLine();

            Console.Write("Telefone: ");
            string telefone = Console.ReadLine();

            Console.Write("Email: ");
            string email = Console.ReadLine();

            try {
                using (StreamWriter sw = new StreamWriter(caminhoArquivo, true)) {
                    sw.WriteLine($"{nome},{telefone},{email}");
                }

                Console.WriteLine("Contato cadastrado com sucesso!");
            }
            catch (Exception ex) {
                Console.WriteLine($"Erro ao cadastrar o contato: {ex.Message}");
            }
        }

        private static void ListarContatos() {
            Console.WriteLine("\nContatos cadastrados:");

            try {
                if (File.Exists(caminhoArquivo)) {
                    using (StreamReader sr = new StreamReader(caminhoArquivo)) {
                        string linha;
                        bool temContatos = false;
                        while ((linha = sr.ReadLine()) != null) {
                            temContatos = true;
                            var contato = linha.Split(',');
                            Console.WriteLine($"Nome: {contato[0]} | Telefone: {contato[1]} | Email: {contato[2]}");
                        }

                        if (!temContatos) {
                            Console.WriteLine("Nenhum contato cadastrado.");
                        }
                    }
                }
                else {
                    Console.WriteLine("Nenhum contato cadastrado.");
                }
            }
            catch (Exception ex) {
                Console.WriteLine($"Erro ao listar os contatos: {ex.Message}");
            }
        }
    }
}