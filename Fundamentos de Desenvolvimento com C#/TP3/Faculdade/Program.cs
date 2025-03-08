namespace Faculdade {
    internal class Program {
        static void Main(string[] args) {
            // Instanciando um objeto Matricula
            Matricula matricula = new Matricula("João Silva", "Engenharia de Software", 12345, "Ativa", "01/01/2024");

            // Exibindo as informações iniciais
            Console.WriteLine("Informações iniciais da matrícula:");
            matricula.ExibirInformacoes();
            Console.WriteLine(); 

            // Trancando a matrícula
            matricula.Trancar();

            // Exibindo as informações após o trancamento
            Console.WriteLine("\nInformações após o trancamento:");
            matricula.ExibirInformacoes();
            Console.WriteLine(); 

            // Reativando a matrícula
            matricula.Reativar();

            // Exibindo as informações após a reativação
            Console.WriteLine("\nInformações após a reativação:");
            matricula.ExibirInformacoes();
        }
    }
}
