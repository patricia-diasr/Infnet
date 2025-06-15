using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class EditClienteModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public EditClienteModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Cliente Cliente { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var cliente =  await _context.Clientes.FirstOrDefaultAsync(m => m.Id == id);

            if (cliente == null) {
                return NotFound();
            }

            Cliente = cliente;

            return Page();
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }

            _context.Attach(Cliente).State = EntityState.Modified;

            try {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException) {
                if (!ClienteExists(Cliente.Id)) {
                    return NotFound();
                }

                else {
                    throw;
                }
            }

            return RedirectToPage("./Index");
        }

        private bool ClienteExists(int id) {
            return _context.Clientes.Any(e => e.Id == id);
        }
    }
}
