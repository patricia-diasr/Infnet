namespace EX9 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite seu salário bruto: ");
            float salarioBruto = float.Parse(Console.ReadLine());

            float descontoImposto = 0;

            if (salarioBruto <= 2259.20f) {
                descontoImposto = 0;
            }

            else if (salarioBruto <= 2826.65f) {
                descontoImposto = (salarioBruto * 0.075f) - 169.44f; 
            }

            else if (salarioBruto <= 3751.05f) {
                descontoImposto = (salarioBruto * 0.15f) - 381.44f; 
            }

            else if (salarioBruto <= 4664.68f) {
                descontoImposto = (salarioBruto * 0.225f) - 662.77f; 
            }

            else {
                descontoImposto = (salarioBruto * 0.275f) - 896.00f; 
            }

            descontoImposto = Math.Max(descontoImposto, 0);
            float salarioLiquido = salarioBruto - descontoImposto;

            Console.WriteLine($"\nO seu salário bruto é: R${salarioBruto:F2}");
            Console.WriteLine($"O desconto de imposto foi de: R${descontoImposto:F2}");
            Console.WriteLine($"O seu salário líquido ficou: R${salarioLiquido:F2}");
        }
    }
}
