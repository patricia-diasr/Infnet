using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;

namespace Turismo.Pages {
    public class CreateCityModel : PageModel {

        // EX 1:
        // [BindProperty]
        // public string NomeCidade { get; set; }

        [BindProperty]
        public EntradaModel Entrada { get; set; }

        public string CidadeRecebida { get; set; }

        public void OnGet() {
        }

        public void OnPost() {
            if (!ModelState.IsValid) {
                return;
            }

            CidadeRecebida = Entrada.NomeCidade;
        }

        public class EntradaModel {
            [Required(ErrorMessage = "O nome da cidade é obrigatório.")]
            [MinLength(3, ErrorMessage = "O nome da cidade deve ter no mínimo 3 caracteres.")]
            public string NomeCidade { get; set; }
        }
    }
}
