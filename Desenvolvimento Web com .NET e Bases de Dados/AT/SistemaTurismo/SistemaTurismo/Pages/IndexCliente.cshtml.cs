using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class IndexClienteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public IndexClienteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public IList<Cliente> Cliente { get;set; } = default!;

        public async Task OnGetAsync() {
            Cliente = await _context.Clientes
                .Where(c => c.DeletedAt == null)
                .ToListAsync();
        }
    }
}
