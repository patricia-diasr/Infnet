using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;

namespace Turismo.Pages
{
    public class CreateMultipleCountriesModel : PageModel
    {
        [BindProperty]
        public List<EntradaModel> Entradas { get; set; }

        public List<Pais> PaisesCadastrados { get; set; } = new();

        public void OnGet() {
            Entradas = new List<EntradaModel>();
            for (int i = 0; i < 5; i++) {
                Entradas.Add(new EntradaModel());
            }
        }

        public void OnPost() {
            if (!ModelState.IsValid) {
                return;
            }

            foreach (var entrada in Entradas) {
                if (!string.IsNullOrWhiteSpace(entrada.NomePais) && !string.IsNullOrWhiteSpace(entrada.CodigoPais)) {
                    PaisesCadastrados.Add(new Pais {
                        Nome = entrada.NomePais,
                        Codigo = entrada.CodigoPais
                    });
                }
            }
        }

        public class EntradaModel {
            [Required(ErrorMessage = "O nome do país é obrigatório.")]
            public string NomePais { get; set; }

            [Required(ErrorMessage = "O código do país é obrigatório.")]
            [StringLength(2, MinimumLength = 2, ErrorMessage = "O código deve ter exatamente 2 letras.")]
            public string CodigoPais { get; set; }
        }

        public class Pais {
            public string Nome { get; set; }
            public string Codigo { get; set; }
        }
    }
}
