package EX10;

import java.io.*;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            FileWriter writer = new FileWriter("compras.txt", true);
            BufferedWriter bufferedWriter = new BufferedWriter(writer);

            for (int i = 1; i <= 3; i++) {
                System.out.println("Cadastro da compra " + i);

                System.out.print("Produto: ");
                String produto = scanner.nextLine();

                System.out.print("Quantidade: ");
                int quantidade = scanner.nextInt();

                System.out.print("Preço unitário: ");
                double precoUnitario = scanner.nextDouble();
                scanner.nextLine();

                bufferedWriter.write("Produto: " + produto + ", Quantidade: " + quantidade + ", Preço unitário: R$ " + precoUnitario);
                bufferedWriter.newLine();
            }

            bufferedWriter.close();
            System.out.println("Compras registradas com sucesso!");
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            BufferedReader bufferedReader = new BufferedReader(new FileReader("compras.txt"));
            System.out.println("\nCompras registradas:");

            String linha;
            while ((linha = bufferedReader.readLine()) != null) {
                System.out.println(linha);
            }

            bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
