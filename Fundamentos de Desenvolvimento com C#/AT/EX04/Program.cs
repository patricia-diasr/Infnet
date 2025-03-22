namespace EX04 {
    internal class Program {
        static void Main(string[] args) {
            DateTime dataAniversario = SolicitarDataAniversario();
            DateTime proximoAniversario = ObterProximoAniversario(dataAniversario);

            int diasRestantes = (proximoAniversario.Date - DateTime.Now.Date).Days;

            if (diasRestantes == 0) {
                Console.WriteLine("Parabéns!!! Hoje é seu aniversário!");
            }
            else if (diasRestantes < 7) {
                Console.WriteLine($"Parabéns!!! Faltam apenas {diasRestantes} dias para o seu aniversário!");
            }
            else {
                Console.WriteLine($"Faltam {diasRestantes} dias para o seu próximo aniversário.");
            }
        }

        static DateTime SolicitarDataAniversario() {
            DateTime dataNascimento;
            bool dataValida;

            do {
                Console.Write("Digite sua data de nascimento (dd/mm/aaaa): ");
                dataValida = DateTime.TryParse(Console.ReadLine(), out dataNascimento);

                if (!dataValida || dataNascimento > DateTime.Now) {
                    Console.WriteLine("Entrada inválida! Por favor, insira uma data de nascimento válida.");
                }

            } while (!dataValida || dataNascimento > DateTime.Now);

            return dataNascimento;
        }

        static DateTime ObterProximoAniversario(DateTime dataNascimento) {
            DateTime proximoAniversario = new DateTime(DateTime.Now.Year, dataNascimento.Month, dataNascimento.Day);

            if (proximoAniversario < DateTime.Now.Date) {
                proximoAniversario = proximoAniversario.AddYears(1);
            }

            return proximoAniversario;
        }
    }
}
