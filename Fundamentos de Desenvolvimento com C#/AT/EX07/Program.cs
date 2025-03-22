namespace EX07 {
    internal class Program {
        static void Main(string[] args) {
            ContaBancaria conta = new ContaBancaria("Patrícia Rodrigues", 0);
            Console.WriteLine($"Titular: {conta.Titular}\n");

            conta.Depositar(500);
            conta.ExibirSaldo(); 

            Console.WriteLine("Tentativa de saque: R$ 700,00");
            conta.Sacar(700);  

            conta.Sacar(200);
            conta.ExibirSaldo();
        }
    }
}
