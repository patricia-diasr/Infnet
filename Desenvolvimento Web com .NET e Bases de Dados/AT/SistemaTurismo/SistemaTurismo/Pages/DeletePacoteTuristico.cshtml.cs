using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DeletePacoteTuristicoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DeletePacoteTuristicoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public PacoteTuristico PacoteTuristico { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var pacoteturistico = await _context.PacotesTuristicos.FirstOrDefaultAsync(m => m.Id == id && m.DeletedAt == null);

            if (pacoteturistico == null) {
                return NotFound();
            }
            else {
                PacoteTuristico = pacoteturistico;
            }

            return Page();
        }

        //12.a - Exclusão Lógica
        public async Task<IActionResult> OnPostAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var pacoteturistico = await _context.PacotesTuristicos.FindAsync(id);
            
            if (pacoteturistico != null) {
                pacoteturistico.DeletedAt = DateTime.Now;
                _context.Attach(pacoteturistico).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }

            return RedirectToPage("./IndexPacoteTuristico");
        }
    }
}
