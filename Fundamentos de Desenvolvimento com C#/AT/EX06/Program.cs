namespace EX06 {
    internal class Program {
        static void Main(string[] args) {
            Aluno aluno = new Aluno("Patrícia Rodrigues", "123456", "Engenharia de Software", 9.5);

            aluno.ExibirDados();
            Console.WriteLine("O aluno está: " + aluno.VerificarAprovacao());
        }
    }
}
