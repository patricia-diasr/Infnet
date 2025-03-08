
namespace EX4 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Insira o seu nome: ");
            string nome = Console.ReadLine();

            Console.Write("Insira a sua idade: ");
            int idade = int.Parse(Console.ReadLine());

            Console.Write("Insira o seu telefone: ");
            string telefone = Console.ReadLine();

            Console.Write("Insira o seu e-mail: ");
            string email = Console.ReadLine();

            Console.WriteLine("\n===== Dados =====");
            Console.WriteLine($"Nome: {nome}");
            Console.WriteLine($"Idade: {idade}");
            Console.WriteLine($"Telefone: {telefone}");
            Console.WriteLine($"E-mail: {email}");
            Console.WriteLine("================");

        }
    }
}
