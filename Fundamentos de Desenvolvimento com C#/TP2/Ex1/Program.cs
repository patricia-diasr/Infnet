namespace EX1 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite sua data de nascimento (dd/MM/yyyy): ");
            String data = Console.ReadLine();

            DateTime dataNascimento = DateTime.Parse(data);
            DateTime hoje = DateTime.Today;

            int anos = hoje.Year - dataNascimento.Year;
            int meses = hoje.Month - dataNascimento.Month;
            int dias = hoje.Day - dataNascimento.Day;

            if (dias < 0) {
                meses--;
                dias += DateTime.DaysInMonth(hoje.Year, (hoje.Month == 1 ? 12 : hoje.Month - 1));
            }

            if (meses < 0) {
                anos--;
                meses += 12;
            }

            Console.WriteLine($"Você tem {anos} anos, {meses} meses e {dias} dias.");
        }
    }
}
