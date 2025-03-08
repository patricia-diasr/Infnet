namespace Faculdade {
    public class Matricula {
        // Atributos
        public string NomeDoAluno { get; set; }
        public string Curso { get; set; }
        public int NumeroMatricula { get; set; }
        public string Situacao { get; set; }
        public string DataInicial { get; set; }

        // Construtor
        public Matricula(string nomeDoAluno, string curso, int numeroMatricula, string situacao, string dataInicial) {
            NomeDoAluno = nomeDoAluno;
            Curso = curso;
            NumeroMatricula = numeroMatricula;
            Situacao = situacao;
            DataInicial = dataInicial;
        }

        // Método para trancar a matrícula (altera a situação para "Trancada")
        public void Trancar() {
            Situacao = "Trancada";
            Console.WriteLine($"A matrícula de {NomeDoAluno} foi trancada.");
        }

        // Método para reativar a matrícula (altera a situação para "Ativa")
        public void Reativar() {
            Situacao = "Ativa";
            Console.WriteLine($"A matrícula de {NomeDoAluno} foi reativada.");
        }

        // Método para exibir as informações da matrícula
        public void ExibirInformacoes() {
            Console.WriteLine($"Nome do Aluno: {NomeDoAluno}");
            Console.WriteLine($"Curso: {Curso}");
            Console.WriteLine($"Situação: {Situacao}");
            Console.WriteLine($"Data Inicial: {DataInicial}");
        }
    }
}
