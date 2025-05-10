using System;

namespace Ex11 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Insira o seu nome: ");
            string nome = Console.ReadLine();

            Console.Write("Insira o seu sobrenome: ");
            string sobrenome = Console.ReadLine();

            Func<string, string, string> processadorNome = Concatenar;
            processadorNome += ConverterMaiusculas;
            processadorNome += RemoverEspacos;

            processadorNome(nome, sobrenome);
        }
        static string Concatenar(string nome, string sobrenome) {
            string resultado = $"{nome} {sobrenome}";
            Console.WriteLine("Nome e sobrenome concatenado: " + resultado);
            return resultado;
        }
        static string ConverterMaiusculas(string nomeCompleto, string _) {
            string resultado = nomeCompleto.ToUpper();
            Console.WriteLine("Nome com letras maiúsculas: " + resultado);
            return resultado;
        }
        static string RemoverEspacos(string nomeCompleto, string _) {
            string resultado = nomeCompleto.Replace(" ", "");
            Console.WriteLine("Nome sem espaços: " + resultado);
            return resultado;
        }
    }
}
