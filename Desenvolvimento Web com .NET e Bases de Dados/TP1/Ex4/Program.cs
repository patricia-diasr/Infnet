namespace Ex4 {
    internal class Program {
        static void Main(string[] args) {
            TemperatureSensor sensor = new TemperatureSensor();

            sensor.TemperatureExceeded += AlertaTemperatura;

            Console.WriteLine("Digite leituras de temperatura (Insira 's' para sair):");

            while (true) {
                Console.Write("Temperatura: ");
                string input = Console.ReadLine();

                if (input.ToLower() == "s") {
                    break;
                }

                double temperatura = double.Parse(input);
                sensor.LerTemperatura(temperatura);
            }
        }

        static void AlertaTemperatura(object sender, double temperatura) {
            Console.WriteLine($"Alerta! Temperatura excedida: {temperatura}°C");
        }
    }
}
