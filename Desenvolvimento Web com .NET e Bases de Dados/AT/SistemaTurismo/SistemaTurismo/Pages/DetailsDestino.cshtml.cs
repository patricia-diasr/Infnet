using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DetailsDestinoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DetailsDestinoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public Destino Destino { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var destino = await _context.Destinos.FirstOrDefaultAsync(m => m.Id == id);
            
            if (destino == null) {
                return NotFound();
            }
            else {
                Destino = destino;
            }

            return Page();
        }
    }
}
