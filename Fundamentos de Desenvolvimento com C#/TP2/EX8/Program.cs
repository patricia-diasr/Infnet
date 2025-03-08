namespace EX8 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite uma nota entre 0 a 10: ");
            float nota = float.Parse(Console.ReadLine());

            if (nota >= 0 && nota <5) {
                Console.WriteLine("Classificação: Insuficiente");
            }
            else if (nota < 7) {
                Console.WriteLine("Classificação: Regular");
            }
            else if (nota <9) {
                Console.WriteLine("Classificação: Bom");
            }
            else if (nota <= 10) {
                Console.WriteLine("Classificação: Excelente");
            }
            else {
                Console.WriteLine("Nota inválida. Por favor, digite uma nota entre 0 e 10.");
            }
        }
    }
}
