package EX06;

public class Veiculo {
    private String placa;
    private String modelo;
    private int anoFabricacao;
    private double kilometragem;

    public Veiculo(String placa, String modelo, int anoFabricacao, double kilometragem) {
        this.placa = placa;
        this.modelo = modelo;
        this.anoFabricacao = anoFabricacao;
        this.kilometragem = kilometragem;
    }

    public void exibirDetalhes() {
        System.out.println("Placa: " + placa);
        System.out.println("Modelo: " + modelo);
        System.out.println("Ano de Fabricação: " + anoFabricacao);
        System.out.println("Quilometragem: " + kilometragem + " km");
        System.out.println("----------------------------");
    }

    public void registrarViagem(double km) {
        if (km > 0) {
            kilometragem += km;
            System.out.println("Viagem registrada! " + km + " km adicionados.");
        } else {
            System.out.println("Erro: A quilometragem da viagem deve ser positiva.");
        }
    }

    public String getPlaca() {
        return placa;
    }

    public void setPlaca(String placa) {
        this.placa = placa;
    }

    public String getModelo() {
        return modelo;
    }

    public void setModelo(String modelo) {
        this.modelo = modelo;
    }

    public int getAnoFabricacao() {
        return anoFabricacao;
    }

    public void setAnoFabricacao(int anoFabricacao) {
        this.anoFabricacao = anoFabricacao;
    }

    public double getKilometragem() {
        return kilometragem;
    }

    public void setKilometragem(double kilometragem) {
        this.kilometragem = kilometragem;
    }
}
