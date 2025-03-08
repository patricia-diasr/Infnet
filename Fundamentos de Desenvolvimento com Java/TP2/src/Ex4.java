import java.time.LocalDate;
import java.time.Period;
import java.util.Scanner;

public class Ex4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Digite o dia do seu nascimento: ");
        int dia = scanner.nextInt();

        System.out.print("Digite o mês do seu nascimento: ");
        int mes = scanner.nextInt();

        System.out.print("Digite o ano do seu nascimento: ");
        int ano = scanner.nextInt();

        LocalDate dataAtual = LocalDate.now();
        LocalDate dataNascimento = LocalDate.of(ano, mes, dia);

        Period periodo = Period.between(dataNascimento, dataAtual);
        int idadeDias = periodo.getYears() * 365 + periodo.getMonths() * 30 + periodo.getDays();

        System.out.println("\nVocê tem " + idadeDias + " dias de vida.");
        scanner.close();
    }
}
