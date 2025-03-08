namespace EX2 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite sua data de nascimento (dd/MM/yyyy): ");
            String data = Console.ReadLine();

            DateTime dataNascimento = DateTime.Parse(data);
            DateTime hoje = DateTime.Today;
            DateTime proximoAniversario = new DateTime(hoje.Year, dataNascimento.Month, dataNascimento.Day);

            if (proximoAniversario < hoje) {
                proximoAniversario = new DateTime(hoje.Year + 1, dataNascimento.Month, dataNascimento.Day);
            }

            TimeSpan distancia = proximoAniversario - hoje;
            int diasFaltando = distancia.Days;


            Console.WriteLine($"Faltam {diasFaltando} dias para o seu aniversário");
        }
    }
}
