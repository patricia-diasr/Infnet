using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class IndexPacoteTuristicoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public IndexPacoteTuristicoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IList<PacoteTuristico> PacoteTuristico { get;set; } = default!;

        public async Task OnGetAsync() {
            PacoteTuristico = await _context.PacotesTuristicos
                .Include(p => p.Destinos)
                    .ThenInclude(pd => pd.Destino)
                .Where(p => p.DeletedAt == null)
                .ToListAsync();
        }
    }
}
