package EX04;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite seu nome: ");
        String nome = scanner.nextLine();

        System.out.print("Digite o valor do empréstimo: R$ ");
        double valorEmprestimo = scanner.nextDouble();

        int parcelas;
        while (true) {
            System.out.print("Digite o número de parcelas (mínimo 6, máximo 48): ");
            parcelas = scanner.nextInt();
            if (parcelas >= 6 && parcelas <= 48) {
                break;
            } else {
                System.out.println("Erro: O número de parcelas deve estar entre 6 e 48.");
            }
        }

        double jurosMensal = 0.03;
        double valorTotalPago = valorEmprestimo * Math.pow(1 + jurosMensal, parcelas);
        double valorParcelaMensal = valorTotalPago / parcelas;

        System.out.println("\nSimulação de Empréstimo - " + nome);
        System.out.println("Valor do Empréstimo: R$ " + String.format("%.2f", valorEmprestimo));
        System.out.println("Número de Parcelas: " + parcelas);
        System.out.println("Valor Total Pago: R$ " + String.format("%.2f", valorTotalPago));
        System.out.println("Valor da Parcela Mensal: R$ " + String.format("%.2f", valorParcelaMensal));

        scanner.close();
    }
}
