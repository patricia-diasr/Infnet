namespace EX03 {
    internal class Program {
        static void Main(string[] args) {
            double numero1 = SolicitarNumero("Insira o primeiro número: ");
            double numero2 = SolicitarNumero("Insira o segundo número: ");
            int operacao = SolicitarOperacao();

            double resultado = RealizarOperacao(numero1, numero2, operacao);
            if (!double.IsNaN(resultado)) {
                char[] operacoes = { '+', '-', 'x', '/' };
                Console.WriteLine($"{numero1} {operacoes[operacao - 1]} {numero2} = {resultado}");
            }

        }

        static double SolicitarNumero(string mensagem) {
            double numero;
            bool numeroValido;

            do {
                Console.Write(mensagem);
                numeroValido = double.TryParse(Console.ReadLine(), out numero);

                if (!numeroValido) {
                    Console.WriteLine("Insira um número válido.");
                }

            } while (!numeroValido);

            return numero;
        }

        static int SolicitarOperacao() {
            int operacao;
            bool operacaoValida;

            Console.WriteLine("=== Operações ===");
            Console.WriteLine("1 - Soma");
            Console.WriteLine("2 - Subtração");
            Console.WriteLine("3 - Multiplicação");
            Console.WriteLine("4 - Divisão");

            do {
                Console.Write("Insira o número da operação desejada (1, 2, 3 ou 4): ");
                operacaoValida = int.TryParse(Console.ReadLine(), out operacao);

                if (!operacaoValida || operacao < 1 || operacao > 4) {
                    Console.WriteLine("Escolha uma operação válida (1, 2, 3 ou 4).");
                }

            } while (!operacaoValida || operacao < 1 || operacao > 4);

            return operacao;
        }

        static double RealizarOperacao(double numero1, double numero2, int operacao) {
            double resultado = 0;
            switch (operacao) {
                case 1:
                    resultado = numero1 + numero2;
                    break;
                case 2:
                    resultado = numero1 - numero2;
                    break;
                case 3:
                    resultado = numero1 * numero2;
                    break;
                case 4:
                    if (numero2 == 0) {
                        Console.WriteLine("Erro: Não é possível dividir por zero!");
                        return double.NaN;
                    }
                    resultado = numero1 / numero2;
                    break;
            }
            return resultado;
        }
    }
}
