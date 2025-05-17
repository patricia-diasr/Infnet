using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;

namespace Turismo.Pages
{
    public class SaveNoteCityDetailModel : PageModel
    {
        [BindProperty]
        public EntradaModel Entrada { get; set; }

        public string LinkDownload { get; set; }

        public void OnGet() {
            Entrada = new EntradaModel();
        }

        public IActionResult OnPost() {
            if (!ModelState.IsValid) {
                return Page();
            }

            var timestamp = DateTime.Now.ToString("yyyyMMddHHmmss");
            var nomeArquivo = $"nota-{Entrada.NomeCidade}-{timestamp}.txt";
            var caminhoPasta = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "files");

            if (!Directory.Exists(caminhoPasta)) {
                Directory.CreateDirectory(caminhoPasta);
            }

            var conteudo = $"Nota sobre a cidade {Entrada.NomeCidade}:\n\n{Entrada.Descricao}";
            var caminhoArquivo = Path.Combine(caminhoPasta, nomeArquivo);
            System.IO.File.WriteAllText(caminhoArquivo, conteudo);

            LinkDownload = $"/files/{nomeArquivo}";

            return Page();
        }

        public class EntradaModel {
            [Required(ErrorMessage = "O nome da cidade � obrigat�rio.")]
            [MinLength(3, ErrorMessage = "O nome da cidade deve ter ao menos 3 caracteres.")]
            public string NomeCidade { get; set; }

            [Required(ErrorMessage = "A descri��o � obrigat�ria.")]
            [MinLength(10, ErrorMessage = "A descri��o deve ter ao menos 10 caracteres.")]
            public string Descricao { get; set; }
        }
    }
}
