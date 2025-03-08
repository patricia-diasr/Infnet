
namespace EX3 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite a 1º data (dd/MM/yyyy): ");

            String input1 = Console.ReadLine();
            DateTime data1 = DateTime.Parse(input1);

            Console.Write("Digite a 2º data (dd/MM/yyyy): ");

            String input2 = Console.ReadLine();
            DateTime data2 = DateTime.Parse(input2);

            if (data1 > data2) {
                (data1, data2) = (data2, data1);
            }

            int anos = data2.Year - data1.Year;
            int meses = data2.Month - data1.Month;
            int dias = data2.Day - data1.Day;

            if (dias < 0) {
                meses--;
                dias += DateTime.DaysInMonth(data1.Year, data1.Month);
            }

            if (meses < 0) {
                anos--;
                meses += 12;
            }

            Console.WriteLine($"O intervalo entre as datas é de {anos} anos, {meses} meses e {dias} dias.");
        }
    }
}
