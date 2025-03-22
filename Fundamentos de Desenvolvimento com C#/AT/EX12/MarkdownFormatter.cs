namespace EX12 {
    internal class MarkdownFormatter : ContatoFormatter {
        public override void ExibirContatos(List<Contato> contatos) {
            Console.WriteLine("## Lista de Contatos\n");
            foreach (var contato in contatos) {
                Console.WriteLine($"- **Nome:** {contato.Nome}\n  📞 Telefone: {contato.Telefone}\n  📧 Email: {contato.Email}\n");
            }
        }
    }
}
