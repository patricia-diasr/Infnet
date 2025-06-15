using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class CreatePacoteTuristicoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public CreatePacoteTuristicoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public PacoteTuristico PacoteTuristico { get; set; } = default!;

        [BindProperty]
        public List<int> DestinosSelecionados { get; set; } = new List<int>();

        public List<SelectListItem> TodosOsDestinos { get; set; } = new List<SelectListItem>();

        public async Task<IActionResult> OnGetAsync() {
            TodosOsDestinos = await _context.Destinos
                .Where(d => d.DeletedAt == null)
                .Select(d => new SelectListItem {
                    Value = d.Id.ToString(),
                    Text = $"{d.Nome} ({d.Pais})"
                })
                .ToListAsync();

            return Page();
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                TodosOsDestinos = await _context.Destinos
                    .Where(d => d.DeletedAt == null)
                    .Select(d => new SelectListItem {
                        Value = d.Id.ToString(),
                        Text = $"{d.Nome} ({d.Pais})"
                    })
                    .ToListAsync();

                return Page();
            }

            PacoteTuristico.Destinos = DestinosSelecionados
                .Select(destinoId => new PacoteTuristicoDestino {
                    DestinoId = destinoId
                }).ToList();

            _context.PacotesTuristicos.Add(PacoteTuristico);
            await _context.SaveChangesAsync();

            return RedirectToPage("./IndexPacoteTuristico");
        }
    }
}
