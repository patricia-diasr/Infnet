import java.util.Scanner;

public class Ex3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        final double taxaDolar = 5.75;
        final double taxaEuro = 6.01;
        final double taxaLibra = 7.29;

        System.out.print("\nDigite o valor em reais: ");
        double valorReais = scanner.nextDouble();

        System.out.println("USD - Dólar");
        System.out.println("EUR - Euro");
        System.out.println("GBP - Libra");

        System.out.print("Escolha a moeda de destino: ");
        String moeda = scanner.next();
        double valorConvertido;

        switch (moeda.toLowerCase()) {
            case "usd":
                valorConvertido = valorReais / taxaDolar;
                break;
            case "eur":
                valorConvertido = valorReais / taxaEuro;
                break;
            case "gbp":
                valorConvertido = valorReais / taxaLibra;
                break;
            default:
                System.out.println("Moeda inválida.");
                scanner.close();
                return;
        }

        System.out.printf("\nO valor convertido é: %.2f %s\n", valorConvertido, moeda);
        scanner.close();
    }
}
