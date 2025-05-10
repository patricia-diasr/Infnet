namespace Ex1
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Informe o preço original do produto: R$ ");
            string input = Console.ReadLine();
            decimal preco = decimal.Parse(input);

            CalculateDiscount calcularDesconto = DescontoDezPorcento;
            decimal precoFinal = calcularDesconto(preco);

            Console.WriteLine($"Você recebeu 10% de desconto! O preço final é de R$ {precoFinal:F2}");
        }

        delegate decimal CalculateDiscount(decimal preco);

        static decimal DescontoDezPorcento(decimal preco) {
            return preco * 0.9m; 
        }

    }
}
