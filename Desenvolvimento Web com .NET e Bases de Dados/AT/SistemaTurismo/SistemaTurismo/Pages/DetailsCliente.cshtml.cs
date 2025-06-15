using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DetailsClienteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DetailsClienteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public Cliente Cliente { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var cliente = await _context.Clientes.FirstOrDefaultAsync(m => m.Id == id);
            
            if (cliente == null) {
                return NotFound();
            }

            else {
                Cliente = cliente;
            }
            
            return Page();
        }
    }
}
