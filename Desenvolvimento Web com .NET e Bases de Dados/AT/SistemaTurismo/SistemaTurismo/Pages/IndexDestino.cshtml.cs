using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class IndexDestinoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public IndexDestinoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IList<Destino> Destino { get;set; } = default!;

        public async Task OnGetAsync() {
            Destino = await _context.Destinos
                .Where(c => c.DeletedAt == null)
                .ToListAsync();
        }
    }
}
