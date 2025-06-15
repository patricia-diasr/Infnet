using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class EditReservaModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public EditReservaModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Reserva Reserva { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var reserva =  await _context.Reservas.FirstOrDefaultAsync(m => m.Id == id);

            if (reserva == null) {
                return NotFound();
            }
            
            Reserva = reserva;
            
            ViewData["ClienteId"] = new SelectList(_context.Clientes, "Id", "Email");
            ViewData["PacoteTuristicoId"] = new SelectList(_context.PacotesTuristicos, "Id", "Titulo");
            
            return Page();
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }

            _context.Attach(Reserva).State = EntityState.Modified;

            try {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException) {
                if (!ReservaExists(Reserva.Id)) {
                    return NotFound();
                }
                else {
                    throw;
                }
            }

            return RedirectToPage("./IndexReserva");
        }

        private bool ReservaExists(int id) {
            return _context.Reservas.Any(e => e.Id == id);
        }
    }
}
