namespace EX08 {
    internal class Program {
        static void Main(string[] args) {
            Funcionario funcionario = new Funcionario("Matheus", "Desenvolvedor", 3000);
            Gerente gerente = new Gerente("Ana", "Gerente de TI", 5000);

            Console.WriteLine($"Salário do {funcionario.Nome} ({funcionario.Cargo}): R${funcionario.CalcularSalario():F2}");
            Console.WriteLine($"Salário do {gerente.Nome} ({gerente.Cargo}): R${gerente.CalcularSalario():F2}");
        }
    }
}
