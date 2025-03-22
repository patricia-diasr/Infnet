package EX02;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite seu nome: ");
        String nome = scanner.nextLine();

        String senha;
        while (true) {
            System.out.print("Digite sua senha: ");
            senha = scanner.nextLine();

            if (senha.length() < 8) {
                System.out.println("Erro: A senha deve ter no mínimo 8 caracteres.");
            } else if (!senha.matches(".*[A-Z].*")) {
                System.out.println("Erro: A senha deve conter pelo menos uma letra maiúscula.");
            } else if (!senha.matches(".*\\d.*")) {
                System.out.println("Erro: A senha deve conter pelo menos um número.");
            } else if (!senha.matches(".*[!@#$%^&*(),.?\":{}|<>].*")) {
                System.out.println("Erro: A senha deve conter pelo menos um caractere especial.");
            } else {
                System.out.println("Senha válida! Cadastro concluído.");
                break;
            }
        }

        scanner.close();
    }
}
