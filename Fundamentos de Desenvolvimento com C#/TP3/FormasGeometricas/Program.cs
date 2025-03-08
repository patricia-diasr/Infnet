namespace FormasGeometricas {
    internal class Program {
        static void Main(string[] args) {
            // Criando um objeto da classe Circulo com raio 3.0
            Circulo circulo = new Circulo(3.0);
            double areaCirculo = circulo.CalcularArea();
            Console.WriteLine($"Área do círculo com raio 3.0: {areaCirculo:N0}");

            // Criando um objeto da classe Esfera com raio 5.0
            Esfera esfera = new Esfera(5.0);
            double volumeEsfera = esfera.CalcularVolume();
            Console.WriteLine($"Volume da esfera com raio 5.0: {volumeEsfera:N0}");
        }
    }
}
