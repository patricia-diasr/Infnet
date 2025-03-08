namespace FormasGeometricas {
    public class Circulo {
        // Atributos
        public double Raio { get; set; }

        // Construtor
        public Circulo(double raio) {
            Raio = raio;
        }

        // Método para calcular área do círculo
        public double CalcularArea() {
            return Math.PI * Raio * Raio;
        }
    }
}
