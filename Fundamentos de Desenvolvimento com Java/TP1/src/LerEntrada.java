// Exercício 9

import java.util.Scanner;

public class LerEntrada {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Qual o seu nome?");
        String nome = scanner.nextLine();

        System.out.println("Qual a sua idade?");
        int idade = scanner.nextInt();

        scanner.close();

        System.out.println("Nome: " + nome + ", Idade: " + idade);

    }
}

// Código com erros produzido no exercício 10

// public class LerEntradaErro {
//     public static void main(String[] args) {
//         Scanner scanner = new Scanner(System.in);
//
//         System.out.println("Qual o seu nome?");
//         String nome = scanner.nextLine();
//
//         System.out.println("Qual a sua idade?");
//         int idade = scanner.nextLine();
//
//         scanner.close();
//
//         System.out.println("Nome: " + nomee + ", Idade: " + idade);
//     }
// }