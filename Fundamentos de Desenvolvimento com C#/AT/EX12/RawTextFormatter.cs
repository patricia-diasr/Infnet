namespace EX12 {
    internal class RawTextFormatter : ContatoFormatter {
        public override void ExibirContatos(List<Contato> contatos) {
            foreach (var contato in contatos) {
                Console.WriteLine($"Nome: {contato.Nome} | Telefone: {contato.Telefone} | Email: {contato.Email}");
            }
        }
    }
}
