using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DeleteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DeleteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Reserva Reserva { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var reserva = await _context.Reservas
                .Include(r => r.Cliente)
                .Include(r => r.PacoteTuristico)
                .FirstOrDefaultAsync(m => m.Id == id && m.DeletedAt == null);

            if (reserva == null) {
                return NotFound();
            }
            else {
                Reserva = reserva;
            }

            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var reserva = await _context.Reservas.FindAsync(id);
            
            if (reserva != null) {
                reserva.DeletedAt = DateTime.Now;
                _context.Attach(reserva).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./IndexReserva");
        }
    }
}
