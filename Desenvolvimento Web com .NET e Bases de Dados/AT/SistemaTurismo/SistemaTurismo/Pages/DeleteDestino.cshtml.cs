using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DeleteDestinoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DeleteDestinoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Destino Destino { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var destino = await _context.Destinos.FirstOrDefaultAsync(m => m.Id == id && m.DeletedAt == null);

            if (destino == null) {
                return NotFound();
            }
            else {
                Destino = destino;
            }

            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var destino = await _context.Destinos.FindAsync(id);
            
            if (destino != null) {
                destino.DeletedAt = DateTime.Now;
                _context.Attach(destino).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./IndexDestino");
        }
    }
}
