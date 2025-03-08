namespace Show {
    internal class Program {
        static void Main(string[] args) {
            // Criando um ingresso para um show
            Ingresso ingresso = new Ingresso("Rock in Rio", 450.00, 100);

            // Exibindo as informações do ingresso
            ingresso.ExibirInformacoes();

            // Atualizando o preço do ingresso
            ingresso.AlterarPreco(600.00);

            // Atualizando a quantidade de ingressos disponíveis
            ingresso.AlterarQuantidade(80);

            // Alternado nome com os Set e exibindo com o Get
            ingresso.NomeDoShow = "Lollapalooza";
            Console.WriteLine(ingresso.NomeDoShow);


            // Exibindo as informações atualizadas
            Console.WriteLine("\nApós atualizações:");
            ingresso.ExibirInformacoes();
        }
    }
}
