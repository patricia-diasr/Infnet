import java.util.Scanner;

public class Ex8 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o comprimento do 1º lado: ");
        double lado1 = scanner.nextDouble();

        System.out.print("Digite o comprimento do 2º lado: ");
        double lado2 = scanner.nextDouble();

        System.out.print("Digite o comprimento do 3º lado: ");
        double lado3 = scanner.nextDouble();

        if (lado1 + lado2 > lado3 && lado1 + lado3 > lado2 && lado2 + lado3 > lado1) {

            if (lado1 == lado2 && lado2 == lado3) {
                System.out.println("O triângulo é equilátero.");
            } else if (lado1 == lado2 || lado1 == lado3 || lado2 == lado3) {
                System.out.println("O triângulo é isósceles.");
            } else {
                System.out.println("O triângulo é escaleno.");
            }

        } else {
            System.out.println("Os lados não formam um triângulo.");
        }

        scanner.close();
    }
}
