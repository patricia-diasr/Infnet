package Supermercado;

public class Main {
    public static void main(String[] args) {
        // Instanciando produtos
        Produto produto1 = new Produto("Arroz", 19.99, 50, "Alimentos", "2025-12-31", "Marca A", 5.0);
        Produto produto2 = new Produto("Leite", 3.49, 100, "Laticínios", "2025-06-30", "Marca B", 1.0);
        Produto produto3 = new Produto("Refrigerante", 7.99, 30, "Bebidas", "2025-05-01", "Marca C", 2.0);

        // Exibindo informações iniciais do produto 1
        System.out.println("Informações iniciais do produto 1:");
        produto1.exibirInformacoes();
        System.out.println("----------------------------");

        // Alterando o preço e a quantidade em estoque do produto 1
        produto1.alterarPreco(22.50); // Novo preço
        produto1.alterarQuantidade(45); // Nova quantidade em estoque

        // Exibindo informações após as alterações do produto 1
        System.out.println("Informações após alterações do produto 1:");
        produto1.exibirInformacoes();
        System.out.println("----------------------------");

        // Exibindo informações iniciais do produto 2
        System.out.println("Informações iniciais do produto 2:");
        produto2.exibirInformacoes();
        System.out.println("----------------------------");

        // Alterando preço e quantidade do produto 2
        produto2.alterarPreco(4.19);
        produto2.alterarQuantidade(120);

        // Exibindo informações após as alterações do produto 2
        System.out.println("Informações após alterações do produto 2:");
        produto2.exibirInformacoes();
        System.out.println("----------------------------");

        // Exibindo informações iniciais do produto 3
        System.out.println("Informações iniciais do produto 3:");
        produto3.exibirInformacoes();
        System.out.println("----------------------------");

        // Alterando preço e quantidade do produto 3
        produto3.alterarPreco(8.49);
        produto3.alterarQuantidade(25);

        // Exibindo informações após as alterações do produto 3
        System.out.println("Informações após alterações do produto 3:");
        produto3.exibirInformacoes();
    }
}
