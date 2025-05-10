namespace Ex2 {
    internal class Program {
        static void Main(string[] args) {

            Console.Write("Digite seu nome: ");
            string nome = Console.ReadLine();

            Console.WriteLine("==== Idiomas ====");
            Console.WriteLine("1 - Português");
            Console.WriteLine("2 - English");
            Console.WriteLine("3 - Español");
            Console.Write("Escolha um idioma: ");

            string idioma = Console.ReadLine();

            Action<string> mensagem;

            switch (idioma) {
                case "1":
                    mensagem = n => Console.WriteLine($"Olá, {nome}! Seja bem-vindo(a)!");
                    break;
                case "2":
                    mensagem = n => Console.WriteLine($"Hello, {nome}! Welcome!");
                    break;
                case "3":
                    mensagem = n => Console.WriteLine($"¡Hola, {nome}! ¡Bienvenido!");
                    break;
                default:
                    Console.WriteLine("Idioma não reconhecido.");
                    return;
            }

            mensagem(nome);
        }
    }
}
