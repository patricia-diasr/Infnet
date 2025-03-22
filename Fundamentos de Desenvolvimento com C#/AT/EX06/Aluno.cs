namespace EX06 {
    internal class Aluno {
        public string Nome { get; set; }
        public string Matricula { get; set; }
        public string Curso { get; set; }
        public double MediaNotas { get; set; }

        public Aluno(string nome, string matricula, string curso, double mediaNotas) {
            Nome = nome;
            Matricula = matricula;
            Curso = curso;
            MediaNotas = mediaNotas;
        }

        public void ExibirDados() {
            Console.WriteLine("Nome: " + Nome);
            Console.WriteLine("Matrícula: " + Matricula);
            Console.WriteLine("Curso: " + Curso);
            Console.WriteLine("Média das Notas: " + MediaNotas);
        }

        public string VerificarAprovacao() {
            if (MediaNotas >= 7) {
                return "Aprovado";
            }
            else {
                return "Reprovado";
            }
        }
    }
}
