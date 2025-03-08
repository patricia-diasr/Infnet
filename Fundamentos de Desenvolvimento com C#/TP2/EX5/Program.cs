namespace EX5 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Insira a temperatura em graus Celsius: ");
            float celsius = float.Parse(Console.ReadLine());

            float kelvin = celsius + 273.15f;
            float fahrenheit = (celsius * 9f / 5f) + 32f;

            Console.WriteLine("===== Temperaturas =====");
            Console.WriteLine($"Celsius: {celsius:F2}ºC");
            Console.WriteLine($"Kelvin: {kelvin:F2}ºK");
            Console.WriteLine($"Fahrenheit: {fahrenheit:F2}ºF");
            Console.WriteLine("========================");

        }
    }
}
