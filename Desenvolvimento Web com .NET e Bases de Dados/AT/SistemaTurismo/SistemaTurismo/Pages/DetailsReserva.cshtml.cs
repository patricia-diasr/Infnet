using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DetailsReservaModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DetailsReservaModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public Reserva Reserva { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var reserva = await _context.Reservas
                .Include(r => r.Cliente)
                .Include(r => r.PacoteTuristico)
                .FirstOrDefaultAsync(m => m.Id == id);

            if (reserva == null) {
                return NotFound();
            }
            else {
                Reserva = reserva;
            }

            return Page();
        }
    }
}
