namespace TP1
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Gato meuGato = new Gato("Loki", 3);

            // Chamando os métodos do objeto
            meuGato.ExibirDetalhes();
            meuGato.Miar();
        }
    }
}
