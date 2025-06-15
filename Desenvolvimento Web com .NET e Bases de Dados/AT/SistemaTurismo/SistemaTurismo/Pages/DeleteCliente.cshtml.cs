using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DeleteClienteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DeleteClienteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Cliente Cliente { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var cliente = await _context.Clientes
                .FirstOrDefaultAsync(m => m.Id == id && m.DeletedAt == null);

            if (cliente == null) {
                return NotFound();
            }

            Cliente = cliente;
            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var cliente = await _context.Clientes.FindAsync(id);
            if (cliente != null) {
                cliente.DeletedAt = DateTime.Now;
                _context.Attach(cliente).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./IndexCliente");
        }

    }
}
