package EX07;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o nome do aluno: ");
        String nome = scanner.nextLine();

        System.out.print("Digite a matrícula do aluno: ");
        String matricula = scanner.nextLine();

        System.out.print("Digite a primeira nota: ");
        double nota1 = scanner.nextDouble();

        System.out.print("Digite a segunda nota: ");
        double nota2 = scanner.nextDouble();

        System.out.print("Digite a terceira nota: ");
        double nota3 = scanner.nextDouble();

        Aluno aluno = new Aluno(nome, matricula, nota1, nota2, nota3);

        System.out.println("\nSituação do aluno " + aluno.getNome() + " (Matrícula: " + aluno.getMatricula() + "):");
        aluno.verificarAprovacao();

        scanner.close();
    }
}
