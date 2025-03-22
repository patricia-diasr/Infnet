package EX08;

import java.text.DecimalFormat;

public class Funcionario {
    protected String nome;
    protected double salarioBase;

    // Construtor
    public Funcionario(String nome, double salarioBase) {
        this.nome = nome;
        this.salarioBase = salarioBase;
    }

    public double calcularSalario() {
        return salarioBase;
    }

    public void exibirDados() {
        DecimalFormat df = new DecimalFormat("#,###.00");
        System.out.println("Nome: " + nome);
        System.out.println("Salário final: R$ " + df.format(calcularSalario()));
    }
}
