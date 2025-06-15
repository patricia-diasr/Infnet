using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class CreateDestinoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public CreateDestinoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IActionResult OnGet() {
            return Page();
        }

        [BindProperty]
        public Destino Destino { get; set; } = default!;

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }
            
            _context.Destinos.Add(Destino);
            await _context.SaveChangesAsync();

            return RedirectToPage("./IndexDestino");
        }
    }
}
