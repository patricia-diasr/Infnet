using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Ex10.Pages
{
    public class AddProductModel : PageModel
    {
        [BindProperty]
        public string NomeProduto { get; set; }

        [BindProperty]
        public decimal PrecoProduto { get; set; }

        public bool Enviado { get; set; } = false;

        public void OnGet() {
        }

        public void OnPost() {
            Enviado = true;
        }
    }
}
