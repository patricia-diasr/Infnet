package EX11;

import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Random random = new Random();
        Scanner scanner = new Scanner(System.in);

        int[] numerosSorteados = new int[6];
        for (int i = 0; i < 6; i++) {
            numerosSorteados[i] = random.nextInt(60) + 1;
        }

        int[] numerosUsuario = new int[6];
        System.out.println("Digite seus 6 números (entre 1 e 60):");
        for (int i = 0; i < 6; i++) {
            System.out.print("Número " + (i + 1) + ": ");
            numerosUsuario[i] = scanner.nextInt();
        }

        int acertos = 0;
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j++) {
                if (numerosSorteados[i] == numerosUsuario[j]) {
                    acertos++;
                }
            }
        }

        System.out.print("Números sorteados: ");
        for (int numero : numerosSorteados) {
            System.out.print(numero + " ");
        }
        System.out.println();

        System.out.println("Você acertou " + acertos + " número(s)!");
    }
}
