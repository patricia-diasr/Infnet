using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;

namespace Turismo.Pages {
    public class CreateCountryModel : PageModel {
        [BindProperty]
        public EntradaModel Entrada { get; set; }

        public string MensagemSucesso { get; set; }

        public void OnGet() {
            Entrada = new EntradaModel();
        }

        public IActionResult OnPost() {
            if (!ModelState.IsValid) {
                return Page();
            }

            if (char.ToUpper(Entrada.CountryName[0]) != char.ToUpper(Entrada.CountryCode[0])) {
                ModelState.AddModelError("Entrada.CountryCode", "O código do país deve começar com a mesma letra do nome.");
                return Page();
            }

            MensagemSucesso = $"País '{Entrada.CountryName}' com código '{Entrada.CountryCode}' salvo com sucesso.";

            return Page();
        }

        public class EntradaModel {
            [Required(ErrorMessage = "O nome do país é obrigatório.")]
            [MinLength(3, ErrorMessage = "O nome do país deve ter ao menos 3 caracteres.")]
            public string CountryName { get; set; }

            [Required(ErrorMessage = "O código do país é obrigatório.")]
            [StringLength(2, MinimumLength = 2, ErrorMessage = "O código do país deve ter exatamente 2 caracteres.")]
            public string CountryCode { get; set; }
        }
    }
}
