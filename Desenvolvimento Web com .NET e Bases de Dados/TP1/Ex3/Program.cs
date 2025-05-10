namespace Ex3 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite o tamanho da base do retângulo: ");
            double baseRetangulo = double.Parse(Console.ReadLine());

            Console.Write("Digite o tamanho altura do retângulo: ");
            double alturaRentangulo = double.Parse(Console.ReadLine());

            Func<double, double, double> calcularArea = (b, h) => b * h;

            double areaRetangulo = calcularArea(baseRetangulo, alturaRentangulo);

            Console.WriteLine($"A área do retângulo é: {areaRetangulo}");
        }
    }
}
