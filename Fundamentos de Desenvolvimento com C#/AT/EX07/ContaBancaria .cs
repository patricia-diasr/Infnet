namespace EX07 {
    internal class ContaBancaria {
        public string Titular { get; set; }
        private decimal Saldo { get; set; }

        public ContaBancaria(string titular, decimal saldoInicial) {
            Titular = titular;
            Saldo = saldoInicial > 0 ? saldoInicial : 0;
        }

        public void Depositar(decimal valor) {
            if (valor > 0) {
                Saldo += valor;
                Console.WriteLine($"Depósito de R$ {valor:F2} realizado com sucesso!");
            }
            else {
                Console.WriteLine("O valor do depósito deve ser positivo!");
            }
        }

        public void Sacar(decimal valor) {
            if (valor > 0 && valor <= Saldo) {
                Saldo -= valor;
                Console.WriteLine($"Saque de R$ {valor:F2} realizado com sucesso!");
            }
            else if (valor > Saldo) {
                Console.WriteLine("Saldo insuficiente para realizar o saque!");
            }
            else {
                Console.WriteLine("O valor do saque deve ser positivo!");
            }
        }

        public void ExibirSaldo() {
            Console.WriteLine($"Saldo atual: R$ {Saldo:F2}");
        }
    }
}
