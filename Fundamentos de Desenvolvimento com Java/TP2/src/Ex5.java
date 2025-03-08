import java.util.Scanner;

public class Ex5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o valor da compra: ");
        double valorCompra = scanner.nextDouble();

        double porcentagemDesconto = 0;

        if (valorCompra > 1000) {
            porcentagemDesconto = 0.10;
        } else if (valorCompra >= 500) {
            porcentagemDesconto =  0.05;
        }

        double valorDesconto = valorCompra * porcentagemDesconto;
        double valorFinal = valorCompra - valorDesconto;

        System.out.println("====== Informações ======");
        System.out.printf("Valor da compra: R$%.2f%n", valorCompra);
        System.out.printf("Desconto: %.0f%%%n", porcentagemDesconto * 100);
        System.out.printf("Valor do desconto: R$%.2f%n", valorDesconto);
        System.out.printf("Valor final a pagar: R$%.2f%n", valorFinal);
        System.out.println("=========================");


        scanner.close();
    }
}
