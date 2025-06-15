using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class DetailsPacoteTuristicoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public DetailsPacoteTuristicoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        public PacoteTuristico PacoteTuristico { get; set; } = default!;

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) {
                return NotFound();
            }

            var pacoteturistico = await _context.PacotesTuristicos.FirstOrDefaultAsync(m => m.Id == id);
            
            if (pacoteturistico == null) {
                return NotFound();
            } else {
                PacoteTuristico = pacoteturistico;
            }

            return Page();
        }
    }
}
