import java.util.Scanner;

public class Ex9 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Cadastre uma senha: ");
        String senha = scanner.nextLine();

        String senhaTentativa;
        do {
            System.out.print("Confirme a sua senha: ");
            senhaTentativa = scanner.nextLine();

            if (!senhaTentativa.equals(senha)) {
                System.out.println("Senha incorreta. Tente novamente.");
            }
        } while (!senhaTentativa.equals(senha));

        System.out.println("Senha correta!");

        scanner.close();
    }
}
