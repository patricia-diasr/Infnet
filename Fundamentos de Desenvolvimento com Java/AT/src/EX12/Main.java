package EX12;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o nome do primeiro usuário: ");
        String usuario1 = scanner.nextLine();
        System.out.print("Digite o nome do segundo usuário: ");
        String usuario2 = scanner.nextLine();

        String[] mensagens = new String[10];

        int contador = 0;

        while (contador < 10) {
            if (contador % 2 == 0) {
                System.out.print(usuario1 + ", digite sua mensagem: ");
                mensagens[contador] = usuario1 + ": " + scanner.nextLine();
            } else {
                System.out.print(usuario2 + ", digite sua mensagem: ");
                mensagens[contador] = usuario2 + ": " + scanner.nextLine();
            }
            contador++;
        }

        System.out.println("\n===== Histórico de Mensagens =====");
        for (String mensagem : mensagens) {
            System.out.println(mensagem);
        }

        System.out.println("\nObrigado por utilizarem o sistema! Boa sorte para vocês! 🚀");

        scanner.close();
    }
}
