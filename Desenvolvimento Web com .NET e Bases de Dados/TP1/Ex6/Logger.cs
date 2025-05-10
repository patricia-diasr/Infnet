namespace Ex6 {
    internal class Logger {
        public void LogToConsole(string messagem) {
            Console.WriteLine($"Console: {messagem}");
            Console.WriteLine("Mensagem gravado no console");
        }

        public void LogToFile(string messagem) {
            string caminhoArquivo = "log.txt";
            string mensagemFormatada = $"{messagem}{Environment.NewLine}";

            File.AppendAllText(caminhoArquivo, mensagemFormatada);
            Console.WriteLine("Mensagem gravado no arquivo txt");
        }

        public void LogToDatabase(string messagem) {
            Console.WriteLine($"Banco: {messagem}");
            Console.WriteLine("Mensagem gravado no banco");
        }
    }
}
