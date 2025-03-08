namespace EX12 {
    internal class Program {
        static void Main(string[] args) {
            Random random = new Random();

            int numeroSorteado = random.Next(1, 101);
            int palpite = 0;
            int tentativas = 0;

            Console.WriteLine("Adivinhe o número entre 1 e 100.");

            while (palpite != numeroSorteado) {
                Console.Write("Digite seu palpite: ");
                palpite = int.Parse(Console.ReadLine());
                tentativas++;

                if (palpite < numeroSorteado) {
                    Console.WriteLine("O número é maior. Tente novamente.");
                }

                else if (palpite > numeroSorteado) {
                    Console.WriteLine("O número é menor. Tente novamente.");
                }

                else {
                    Console.WriteLine("Parabéns! Você acertou o número " + numeroSorteado + " após " + tentativas + " tentativas!");
                }
            }
        }
    }
}
