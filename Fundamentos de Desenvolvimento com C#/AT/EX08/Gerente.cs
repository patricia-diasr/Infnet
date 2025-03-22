namespace EX08 {
    internal class Gerente : Funcionario {
        public Gerente(string nome, string cargo, double salarioBase)
            : base(nome, cargo, salarioBase) {
        }

        public override double CalcularSalario() {
            return SalarioBase * 1.20; 
        }
    }
}
