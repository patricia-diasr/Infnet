import java.util.Random;
import java.util.Scanner;

public class Ex10 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        int numeroSorteado = random.nextInt(100) + 1;
        int palpite = 0;
        int tentativas = 0;

        System.out.println("Adivinhe o número entre 1 e 100.");

        while (palpite != numeroSorteado) {
            System.out.print("Digite seu palpite: ");
            palpite = scanner.nextInt();
            tentativas++;

            if (palpite < numeroSorteado) {
                System.out.println("O número é maior. Tente novamente.");
            } else if (palpite > numeroSorteado) {
                System.out.println("O número é menor. Tente novamente.");
            } else {
                System.out.println("Parabéns! Você acertou o número " + numeroSorteado + " após " + tentativas  + " tentativas!");
            }
        }

        scanner.close();
    }
}
