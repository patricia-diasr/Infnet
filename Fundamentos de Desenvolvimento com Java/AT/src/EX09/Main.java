package EX09;

public class Main {
    public static void main(String[] args) {
        ContaBancaria conta = new ContaBancaria("Pedro", 1000.00);

        conta.exibirSaldo();
        conta.depositar(500.00);

        conta.exibirSaldo();
        conta.sacar(200.00);

        conta.exibirSaldo();
        conta.sacar(2000.00);
    }
}
