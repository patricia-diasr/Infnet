namespace Ex6 {
    internal class Program {
        static void Main(string[] args) {
            Logger logger = new Logger();

            Action<string> logDelegate = logger.LogToConsole;
            logDelegate += logger.LogToFile;
            logDelegate += logger.LogToDatabase;

            Console.Write("Insira a mensagem: ");
            string mensagem = Console.ReadLine();

            logDelegate(mensagem);
        }
    }
}
