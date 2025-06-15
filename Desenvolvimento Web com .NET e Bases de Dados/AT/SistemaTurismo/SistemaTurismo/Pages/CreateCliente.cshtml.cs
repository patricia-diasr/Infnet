using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class CreateClienteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public CreateClienteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IActionResult OnGet() {
            return Page();
        }

        [BindProperty]
        public Cliente Cliente { get; set; } = default!;

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }

            _context.Clientes.Add(Cliente);
            await _context.SaveChangesAsync();

            return RedirectToPage("./IndexCliente");
        }
    }
}
