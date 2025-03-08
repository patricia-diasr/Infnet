import java.util.Scanner;

public class Ex7 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite seu salário bruto anual: R$ ");
        double salarioAnual = scanner.nextDouble();

        double imposto;
        double salarioMensal = salarioAnual / 12;

        if (salarioMensal <= 2259.20) {
            imposto = 0.0;
        } else if (salarioMensal <= 2826.65) {
            imposto = (salarioMensal * 0.075) - 169.44;
        } else if (salarioMensal <= 3751.05) {
            imposto = (salarioMensal * 0.15) - 381.44;
        } else if (salarioMensal <= 4664.68) {
            imposto = (salarioMensal * 0.225) - 662.77;
        } else {
            imposto = (salarioMensal * 0.275) - 896.00;
        }

        double salarioLiquido = (salarioAnual / 12) - imposto;

        System.out.printf("O imposto de renda a pagar é: R$ %.2f%n", imposto);
        System.out.printf("Seu salário líquido é: R$ %.2f%n", salarioLiquido);

        scanner.close();
    }
}
