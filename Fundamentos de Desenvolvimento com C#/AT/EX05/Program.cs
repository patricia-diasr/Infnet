namespace EX05 {
    internal class Program {
        static void Main(string[] args) {
            DateTime dataFormatura = new DateTime(2027, 12, 1);
            DateTime dataAtual = SolicitarData();

            if (dataAtual > DateTime.Now) {
                Console.WriteLine("Erro: A data informada não pode ser no futuro!");
                return;
            }

            if (dataAtual > dataFormatura) {
                Console.WriteLine("Parabéns! Você já deveria estar formado!");
                return;
            }

            var diferenca = dataFormatura - dataAtual;

            int anos = dataFormatura.Year - dataAtual.Year;
            if (dataAtual > dataFormatura.AddYears(-anos)) {
                anos--;
            }

            int meses = dataFormatura.Month - dataAtual.Month + (12 * anos);
            if (dataAtual.Day > dataFormatura.Day) {
                meses--;
            }

            int dias = (dataFormatura - dataAtual.AddMonths(meses)).Days;

            Console.WriteLine($"Faltam {anos} anos, {meses % 12} meses e {dias} dias para sua formatura!");

            if (anos == 0 && meses < 6) {
                Console.WriteLine("A reta final chegou! Prepare-se para a formatura!");
            }
        }

        static DateTime SolicitarData() {
            DateTime data;
            bool dataValida;

            do {
                Console.Write("Digite a data atual (dd/mm/aaaa): ");
                dataValida = DateTime.TryParse(Console.ReadLine(), out data);

                if (!dataValida) {
                    Console.WriteLine("Entrada inválida! Por favor, insira uma data válida.");
                }

            } while (!dataValida);

            return data;
        }
    }
}
