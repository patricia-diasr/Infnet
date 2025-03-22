using System.Runtime.Serialization;

namespace EX12 {
    internal class Program {
        private static string caminhoArquivo = "contatos.txt";
        static void Main(string[] args) {
            List<Contato> contatos = CarregarContatos();

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
                        contatos = CarregarContatos(); 
                        break;

                    case "2":
                        ExibirContatos(contatos);
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

        private static List<Contato> CarregarContatos() {
            List<Contato> contatos = new List<Contato>();

            try {
                if (File.Exists(caminhoArquivo)) {
                    using (StreamReader sr = new StreamReader(caminhoArquivo)) {
                        string linha;
                        while ((linha = sr.ReadLine()) != null) {
                            var dados = linha.Split(',');
                            var contato = new Contato(dados[0], dados[1], dados[2]);
                            contatos.Add(contato);
                        }
                    }
                }
            }
            catch (Exception ex) {
                Console.WriteLine($"Erro ao carregar os contatos: {ex.Message}");
            }

            return contatos;
        }

        private static void ExibirContatos(List<Contato> contatos) {
            Console.WriteLine("\nEscolha o formato de exibição:");
            Console.WriteLine("1. Markdown");
            Console.WriteLine("2. Tabela");
            Console.WriteLine("3. Texto Puro");

            Console.Write("Escolha uma opção: ");
            string formatoEscolhido = Console.ReadLine();
            ContatoFormatter formatter;

            switch (formatoEscolhido) {
                case "1":
                    formatter = new MarkdownFormatter();
                    break;
                case "2":
                    formatter = new TabelaFormatter();
                    break;
                case "3":
                    formatter = new RawTextFormatter();
                    break;
                default:
                    throw new ArgumentException("Formato inválido.");
            }

            formatter.ExibirContatos(contatos);
        }
    }
}
