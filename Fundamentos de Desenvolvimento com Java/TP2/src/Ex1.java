import java.util.Scanner;

public class Ex1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite seu nome completo: ");
        String nome = scanner.nextLine();

        System.out.print("Digite sua idade: ");
        int idade = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Digite o nome da sua mãe: ");
        String nomeMae = scanner.nextLine();

        System.out.print("Digite o nome do seu pai: ");
        String nomePai = scanner.nextLine();

        System.out.println("====== Informações ======");
        System.out.println("Nome: " + nome);
        System.out.println("Idade: " + idade);
        System.out.println("Nome da Mãe: " + nomeMae);
        System.out.println("Nome do Pai: " + nomePai);
        System.out.println("=========================");


        if (nome.length() > nomeMae.length()) {
            System.out.println("Seu nome tem mais letras que o nome da sua mãe.");
        } else {
            System.out.println("Seu nome não tem mais letras que o nome da sua mãe.");
        }

        if (nome.length() > nomePai.length()) {
            System.out.println("Seu nome tem mais letras que o nome do seu pai.");
        } else {
            System.out.println("Seu nome não tem mais letras que o nome do seu pai.");
        }

        scanner.close();
    }
}
