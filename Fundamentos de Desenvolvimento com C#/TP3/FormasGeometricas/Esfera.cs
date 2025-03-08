namespace FormasGeometricas {
    public class Esfera {
        // Atributos
        public double Raio { get; set; }

        // Construtor
        public Esfera(double raio) {
            Raio = raio;
        }

        // Método para calcular área do círculo
        public double CalcularVolume() {
            return (4.0 / 3.0) * Math.PI * Math.Pow(Raio, 3);
        }
    }
}
