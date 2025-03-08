namespace Variaveis {
    internal class Program {
        static void Main(string[] args) {
            Console.WriteLine("Qual o seu nome?");
            string nome = Console.ReadLine();

            Console.WriteLine("Qual a sua idade?");
            int idade = int.Parse(Console.ReadLine());

            Console.WriteLine("Qual a sua altura?");
            double altura = double.Parse(Console.ReadLine());

            Console.WriteLine();
            Console.WriteLine("Meu nome é " + nome + ", minha idade é " + idade + " e minha altura é " + altura);
        }
    }
}
