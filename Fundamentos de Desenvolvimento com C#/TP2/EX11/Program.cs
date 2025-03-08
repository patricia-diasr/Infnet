namespace EX11 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite um número inteiro: ");
            int numero = int.Parse(Console.ReadLine());

            Console.WriteLine($"\n===== Tabuada do {numero} =====");
            for (int i = 1; i <= 10; i++) {
                int resultado = numero * i;
                Console.WriteLine($"{numero} x {i} = {resultado}");
            }
        }
    }
}
