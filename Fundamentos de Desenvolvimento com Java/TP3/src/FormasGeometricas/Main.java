package FormasGeometricas;

import java.text.DecimalFormat;

public class Main {
    public static void main(String[] args) {
        DecimalFormat df = new DecimalFormat("#,##");

        // Criando um objeto da classe Circulo com raio 3.0
        Circulo circulo = new Circulo(3.0);
        double areaCirculo = circulo.calcularArea();
        System.out.println("Área do círculo com raio 3.0: " + df.format(areaCirculo));

        // Criando um objeto da classe Esfera com raio 5.0
        Esfera esfera = new Esfera(5.0);
        double volumeEsfera = esfera.calcularVolume();
        System.out.println("Volume da esfera com raio 5.0: " + df.format(volumeEsfera));
    }
}
