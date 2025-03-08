namespace EX7 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite um número inteiro: ");
            int numero = int.Parse(Console.ReadLine());

            if (numero % 2 == 0) {
                Console.WriteLine($"O número {numero} é par");
            }

            else {
                Console.WriteLine($"O número {numero} é impar");
            }

        }
    }
}
