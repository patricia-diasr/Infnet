using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class EditPacoteTuristicoModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public EditPacoteTuristicoModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public PacoteTuristico PacoteTuristico { get; set; } = default!;

        [BindProperty]
        public List<int> DestinosSelecionados { get; set; } = new List<int>();

        public List<SelectListItem> TodosOsDestinos { get; set; } = new List<SelectListItem>();

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null) return NotFound();

            PacoteTuristico = await _context.PacotesTuristicos
                .Include(p => p.Destinos)
                .ThenInclude(pd => pd.Destino)
                .FirstOrDefaultAsync(p => p.Id == id);

            if (PacoteTuristico == null) return NotFound();

            DestinosSelecionados = PacoteTuristico.Destinos.Select(d => d.DestinoId).ToList();

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

            var pacoteExistente = await _context.PacotesTuristicos
                .Include(p => p.Destinos)
                .FirstOrDefaultAsync(p => p.Id == PacoteTuristico.Id);

            if (pacoteExistente == null) return NotFound();

            pacoteExistente.Titulo = PacoteTuristico.Titulo;
            pacoteExistente.DataInicio = PacoteTuristico.DataInicio;
            pacoteExistente.CapacidadeMaxima = PacoteTuristico.CapacidadeMaxima;
            pacoteExistente.Preco = PacoteTuristico.Preco;

            pacoteExistente.Destinos.Clear();

            foreach (var destinoId in DestinosSelecionados) {
                pacoteExistente.Destinos.Add(new PacoteTuristicoDestino {
                    PacoteTuristicoId = PacoteTuristico.Id,
                    DestinoId = destinoId
                });
            }

            await _context.SaveChangesAsync();

            return RedirectToPage("./IndexPacoteTuristico");
        }

        private bool PacoteTuristicoExists(int id) {
            return _context.PacotesTuristicos.Any(e => e.Id == id);
        }
    }
}
