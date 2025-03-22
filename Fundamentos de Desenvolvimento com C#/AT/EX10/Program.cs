namespace EX10 {
    internal class Program {
        static void Main(string[] args) {
            Random random = new Random();
            int numeroAleatorio = random.Next(1, 51);

            int tentativas = 5;
            bool acertou = false;

            Console.WriteLine("Adivinhe um número de 1 a 50.");
            Console.WriteLine("Você tem 5 tentativas.");

            while (tentativas > 0 && !acertou) {
                try {
                    Console.WriteLine($"\nTentativas restantes: {tentativas}");
                    Console.Write("Digite seu palpite: ");
                    int palpite = int.Parse(Console.ReadLine());

                    if (palpite < 1 || palpite > 50) {
                        Console.WriteLine("Erro! O número deve estar entre 1 e 50.");
                    }
                    else {
                        if (palpite == numeroAleatorio) {
                            acertou = true;
                            Console.WriteLine("Parabéns! Você acertou o número!");
                        }
                        else if (palpite < numeroAleatorio) {
                            Console.WriteLine("O número é maior. Tente novamente.");
                        }
                        else {
                            Console.WriteLine("O número é menor. Tente novamente.");
                        }
                    }

                    tentativas--;
                }
                catch (FormatException) {
                    Console.WriteLine("Erro! Por favor, insira um número válido.");
                }
            }

            if (!acertou) {
                Console.WriteLine($"\nVocê perdeu! O número era {numeroAleatorio}.");
            }

        }
    }
}
