package Banco;

public class Main {
    public static void main(String[] args) {
        // Criando uma conta
        Conta minhaConta = new Conta("João Silva", 12345, "001", 1000.0, "01/03/2025");

        // Exibindo saldo inicial
        System.out.println("Saldo inicial: R$" + minhaConta.getSaldo());

        // Testando depósito
        minhaConta.deposita(500.0);
        System.out.println("Saldo após depósito de R$500: R$" + minhaConta.getSaldo());

        // Testando saque
        minhaConta.saca(200.0);
        System.out.println("Saldo após saque de R$200: R$" + minhaConta.getSaldo());

        // Testando rendimento
        double rendimento = minhaConta.calculaRendimento();
        System.out.println("Rendimento mensal: R$" + rendimento);
    }
}
