package EX06;

public class Main {
    public static void main(String[] args) {
        Veiculo veiculo1 = new Veiculo("LMN-9876", "Fiesta", 2018, 45000);
        Veiculo veiculo2 = new Veiculo("UVW-1234", "Uno", 2016, 62000);

        System.out.println("Detalhes do Veículo 1:");
        veiculo1.exibirDetalhes();

        System.out.println("Detalhes do Veículo 2:");
        veiculo2.exibirDetalhes();

        veiculo1.registrarViagem(150);
        veiculo2.registrarViagem(200);

        System.out.println("Detalhes após registrar viagens:");
        veiculo1.exibirDetalhes();
        veiculo2.exibirDetalhes();
    }
}
