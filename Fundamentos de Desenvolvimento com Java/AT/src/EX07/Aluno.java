package EX07;

import java.text.DecimalFormat;

public class Aluno {
    private String nome;
    private String matricula;
    private double nota1;
    private double nota2;
    private double nota3;

    public Aluno(String nome, String matricula, double nota1, double nota2, double nota3) {
        this.nome = nome;
        this.matricula = matricula;
        this.nota1 = nota1;
        this.nota2 = nota2;
        this.nota3 = nota3;
    }

    public double calcularMedia() {
        return (nota1 + nota2 + nota3) / 3;
    }

    public void verificarAprovacao() {
        double media = calcularMedia();
        DecimalFormat df = new DecimalFormat("#.00");

        if (media >= 7) {
            System.out.println("Aluno aprovado com média: " + df.format(media));
        } else {
            System.out.println("Aluno reprovado com média: " + df.format(media));
        }
    }

    public String getNome() {
        return nome;
    }

    public String getMatricula() {
        return matricula;
    }
}
