namespace EX08 {
    internal class Funcionario {
        public string Nome { get; set; }
        public string Cargo { get; set; }
        public double SalarioBase { get; set; }

        public Funcionario(string nome, string cargo, double salarioBase) {
            Nome = nome;
            Cargo = cargo;
            SalarioBase = salarioBase;
        }

        public virtual double CalcularSalario() {
            return SalarioBase;
        }
    }
}
