package EX03;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite seu nome: ");
        String nome = scanner.nextLine();

        System.out.print("Digite seu salário mensal: R$ ");
        double salarioMensal = scanner.nextDouble();

        double salarioAnual = salarioMensal * 12;

        double impostoAnual = 0.0;
        double impostoMensal = 0.0;

        if (salarioAnual <= 22847.76) {
            impostoAnual = 0.0;
        } else if (salarioAnual <= 33919.80) {
            impostoAnual = salarioAnual * 0.075;
        } else if (salarioAnual <= 45012.60) {
            impostoAnual = salarioAnual * 0.15;
        } else {
            impostoAnual = salarioAnual * 0.275;
        }

        if (impostoAnual > 0) {
            impostoMensal = impostoAnual / 12;
        }

        double salarioLiquidoAnual = salarioAnual - impostoAnual;
        double salarioLiquidoMensal = salarioMensal - impostoMensal;

        System.out.println("Nome: " + nome);
        System.out.println("Salário Mensal: R$ " + String.format("%.2f", salarioMensal));
        System.out.println("Imposto de Renda Mensal: R$ " + String.format("%.2f", impostoMensal));
        System.out.println("Salário Líquido Mensal: R$ " + String.format("%.2f", salarioLiquidoMensal));

        System.out.println("Salário Anual: R$ " + String.format("%.2f", salarioAnual));
        System.out.println("Imposto de Renda Anual: R$ " + String.format("%.2f", impostoAnual));
        System.out.println("Salário Líquido Anual: R$ " + String.format("%.2f", salarioLiquidoAnual));

        scanner.close();
    }
}
