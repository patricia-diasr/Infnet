using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

// 8 - Sistema de Notas com Leitura e Escrita de Arquivos
namespace SistemaTurismo.Pages {
    public class ViewNotesModel : PageModel {
        private readonly IWebHostEnvironment _ambiente;

        public ViewNotesModel(IWebHostEnvironment ambiente) {
            _ambiente = ambiente;
        }

        [BindProperty]
        public string TituloNota { get; set; } = string.Empty;

        [BindProperty]
        public string ConteudoNota { get; set; } = string.Empty;

        public List<string> ArquivosNotas { get; set; } = new();

        public string? ConteudoNotaSelecionada { get; set; }
        public string? NomeArquivoSelecionado { get; set; }

        public void OnGet(string? nomeArquivo = null) {
            var caminho = Path.Combine(_ambiente.WebRootPath, "files");

            if (!Directory.Exists(caminho)) {
                Directory.CreateDirectory(caminho);
            }

            ArquivosNotas = Directory.GetFiles(caminho, "*.txt")
                                     .Select(f => Path.GetFileName(f))
                                     .ToList();

            if (!string.IsNullOrEmpty(nomeArquivo)) {
                var caminhoArquivo = Path.Combine(caminho, nomeArquivo);
                if (System.IO.File.Exists(caminhoArquivo)) {
                    ConteudoNotaSelecionada = System.IO.File.ReadAllText(caminhoArquivo);
                    NomeArquivoSelecionado = nomeArquivo;
                }
            }
        }

        public IActionResult OnPost() {
            if (!ModelState.IsValid || string.IsNullOrWhiteSpace(TituloNota) || string.IsNullOrWhiteSpace(ConteudoNota)) {
                return Page();
            }

            var tituloSeguro = Path.GetFileNameWithoutExtension(TituloNota);
            var nomeArquivo = $"{tituloSeguro}.txt";
            var caminho = Path.Combine(_ambiente.WebRootPath, "files");

            if (!Directory.Exists(caminho)) {
                Directory.CreateDirectory(caminho);
            }

            var caminhoCompleto = Path.Combine(caminho, nomeArquivo);
            System.IO.File.WriteAllText(caminhoCompleto, ConteudoNota);

            return RedirectToPage("ViewNotes");
        }
    }
}
