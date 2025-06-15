using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class EditDestinoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public EditDestinoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Destino Destino { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var destino =  await _context.Destinos.FirstOrDefaultAsync(m => m.Id == id);
            
            if (destino == null) {
                return NotFound();
            }

            Destino = destino;
            
            return Page();
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }

            _context.Attach(Destino).State = EntityState.Modified;

            try {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException) {
                if (!DestinoExists(Destino.Id)) {
                    return NotFound();
                }
                else {
                    throw;
                }
            }

            return RedirectToPage("./IndexDestino");
        }

        private bool DestinoExists(int id) {
            return _context.Destinos.Any(e => e.Id == id);
        }
    }
}
