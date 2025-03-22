package EX08;

public class Main {
    public static void main(String[] args) {
        Funcionario gerente = new Gerente("Maria Souza", 5000.00);
        Funcionario estagiario = new Estagiario("Carlos Oliveira", 1500.00);

        System.out.println("Funcionário 1 (Gerente):");
        gerente.exibirDados();
        System.out.println();

        System.out.println("Funcionário 2 (Estagiário):");
        estagiario.exibirDados();
    }
}
