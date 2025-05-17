using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Turismo.Pages
{
    public class ListNotesModel : PageModel
    {
        public List<string> Arquivos { get; set; } = new List<string>();
        public string ConteudoArquivo { get; set; }
        public string ArquivoSelecionado { get; set; }

        public void OnGet(string nomeArquivo) {
            var caminhoPasta = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "files");

            if (Directory.Exists(caminhoPasta)) {
                Arquivos = Directory.GetFiles(caminhoPasta, "*.txt")
                                    .Select(f => Path.GetFileName(f))
                                    .ToList();

                if (!string.IsNullOrEmpty(nomeArquivo)) {
                    var caminhoArquivo = Path.Combine(caminhoPasta, nomeArquivo);
                    if (System.IO.File.Exists(caminhoArquivo)) {
                        ConteudoArquivo = System.IO.File.ReadAllText(caminhoArquivo);
                        ArquivoSelecionado = nomeArquivo;
                    }
                }
            }
        }
    }
}
