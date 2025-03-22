namespace EX09 {
    internal class Program {
        static void Main(string[] args) {
            Console.WriteLine("Escolha a versão do sistema:");
            Console.WriteLine("1. Manipulação de Arrays");
            Console.WriteLine("2. Persistência com Arquivos");

            Console.Write("Escolha uma opção: ");
            string opcao = Console.ReadLine();

            switch (opcao) {
                case "1":
                    new Versao1().Menu();
                    break;

                case "2":
                    new Versao2().Menu();
                    break;

                default:
                    Console.WriteLine("Opção inválida!");
                    break;
            }
        }
    }
}
