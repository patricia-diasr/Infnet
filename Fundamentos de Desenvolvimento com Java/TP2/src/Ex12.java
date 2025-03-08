import java.util.Scanner;

public class Ex12 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite uma frase: ");
        String frase = scanner.nextLine();

        String[] palavras = frase.split("\\s+");
        int numeroDePalavras = 0;

        for (String palavra : palavras) {
            if (!palavra.isEmpty()) {
                numeroDePalavras++;
            }
        }

        System.out.println("A frase contém " + numeroDePalavras + " palavras.");
        scanner.close();
    }
}
