import java.util.Scanner;

public class Ex2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite a 1º nota: ");
        double nota1 = scanner.nextDouble();

        System.out.print("Digite a 2º nota: ");
        double nota2 = scanner.nextDouble();

        System.out.print("Digite a 3º nota: ");
        double nota3 = scanner.nextDouble();

        System.out.print("Digite a 4º nota: ");
        double nota4 = scanner.nextDouble();

        double media = (nota1 + nota2 + nota3 + nota4) / 4;
        System.out.println("Sua média foi: " + media);

        if (media >= 7) {
            System.out.println("Você foi aprovado.");
        } else if (media >= 5) {
            System.out.println("Você está em recuperação.");
        } else {
            System.out.println("Você foi reprovado.");
        }

        scanner.close();
    }
}
