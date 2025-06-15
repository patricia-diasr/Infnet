using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class IndexReservaModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public IndexReservaModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IList<Reserva> Reserva { get;set; } = default!;

        public async Task OnGetAsync() {
            Reserva = await _context.Reservas
                .Include(r => r.Cliente)
                .Include(r => r.PacoteTuristico)
                .Where(c => c.DeletedAt == null)
                .ToListAsync();
        }
    }
}
