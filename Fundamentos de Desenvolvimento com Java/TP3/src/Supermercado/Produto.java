package Supermercado;

public class Produto {

    // Nome do produto para identificação no sistema
    private String nome;

    // Preço unitário do produto, essencial para cálculos financeiros e vendas
    private double preco;

    // Quantidade disponível no estoque, usada para controle de reposição
    private int quantidadeEmEstoque;

    // Categoria do produto (ex.: bebidas, laticínios), útil para organização e buscas
    private String categoria;

    // Data de validade, fundamental para o controle de produtos perecíveis
    private String dataValidade;

    // Marca do produto, permitindo diferenciar fabricantes e qualidade
    private String marca;

    // Peso ou volume do produto, importante para precificação e logística
    private double peso;

    // Construtor para inicializar todos os atributos
    // O construtor facilita a criação do objeto, permitindo inicializar todos os atributos de uma vez
    public Produto(String nome, double preco, int quantidadeEmEstoque,
                   String categoria, String dataValidade, String marca, double peso) {
        this.nome = nome;
        this.preco = preco;
        this.quantidadeEmEstoque = quantidadeEmEstoque;
        this.categoria = categoria;
        this.dataValidade = dataValidade;
        this.marca = marca;
        this.peso = peso;
    }

    // Getters e Setters

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public double getPreco() {
        return preco;
    }

    public void setPreco(double preco) {
        this.preco = preco;
    }

    public int getQuantidadeEmEstoque() {
        return quantidadeEmEstoque;
    }

    public void setQuantidadeEmEstoque(int quantidadeEmEstoque) {
        this.quantidadeEmEstoque = quantidadeEmEstoque;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public String getDataValidade() {
        return dataValidade;
    }

    public void setDataValidade(String dataValidade) {
        this.dataValidade = dataValidade;
    }

    public String getMarca() {
        return marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    public double getPeso() {
        return peso;
    }

    public void setPeso(double peso) {
        this.peso = peso;
    }

    // Método para alterar o preço do produto
    public void alterarPreco(double novoPreco) {
        this.preco = novoPreco;
    }

    // Método para alterar a quantidade em estoque
    public void alterarQuantidade(int novaQuantidade) {
        this.quantidadeEmEstoque = novaQuantidade;
    }

    // Método para exibir todas as informações do produto
    public void exibirInformacoes() {
        System.out.println("Nome: " + this.nome);
        System.out.println("Preço: R$ " + this.preco);
        System.out.println("Quantidade em estoque: " + this.quantidadeEmEstoque);
        System.out.println("Categoria: " + this.categoria);
        System.out.println("Data de Validade: " + this.dataValidade);
        System.out.println("Marca: " + this.marca);
        System.out.println("Peso: " + this.peso + "kg");
    }
}
