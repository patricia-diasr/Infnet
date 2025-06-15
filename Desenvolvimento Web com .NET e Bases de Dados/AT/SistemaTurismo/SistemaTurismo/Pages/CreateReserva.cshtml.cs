using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;
using System.Linq.Expressions;
using System;

namespace SistemaTurismo.Pages {
    [Authorize]
    public class CreateReservaModel : PageModel {
        private readonly SistemaTurismo.Data.SistemaTurismoContext _context;

        public CreateReservaModel(SistemaTurismo.Data.SistemaTurismoContext context) {
            _context = context;
        }

        [BindProperty]
        public Reserva Reserva { get; set; } = default!;

        public decimal PrecoOriginal { get; set; } = 100m;
        public decimal PrecoComDesconto { get; set; }

        public IActionResult OnGet() {
            ViewData["ClienteId"] = new SelectList(
                _context.Clientes
                    .Where(c => c.DeletedAt == null),
                "Id", "Email"
            );

            ViewData["PacoteTuristicoId"] = new SelectList(
                _context.PacotesTuristicos
                    .Where(p => p.DeletedAt == null),
                "Id", "Titulo"
            );

            CalculateDelegate descontoDelegate = DescontoService.AplicarDesconto;
            PrecoComDesconto = descontoDelegate(PrecoOriginal);

            return Page();
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                return Page();
            }

            var pacote = await _context.PacotesTuristicos
                .Include(p => p.Reservas)
                .FirstOrDefaultAsync(p => p.Id == Reserva.PacoteTuristicoId);

            if (pacote == null) {
                ModelState.AddModelError(string.Empty, "Pacote turístico não encontrado.");
                return Page();
            }

            if (pacote.DataInicio <= DateTime.Today) {
                ModelState.AddModelError(string.Empty, "Não é possível reservar pacotes com data passada.");
                return Page();
            }

            var reservasAtivas = pacote.Reservas.Count(r => r.DeletedAt == null);
            if (reservasAtivas >= pacote.CapacidadeMaxima) {
                ModelState.AddModelError(string.Empty, "Capacidade máxima do pacote atingida.");
                return Page();
            }

            bool reservaDuplicada = await _context.Reservas.AnyAsync(r =>
                r.ClienteId == Reserva.ClienteId &&
                r.PacoteTuristicoId == Reserva.PacoteTuristicoId &&
                r.DataReserva.Date == Reserva.DataReserva.Date &&
                r.DeletedAt == null
            );

            if (reservaDuplicada) {
                ModelState.AddModelError(string.Empty, "O cliente já possui uma reserva para esse pacote na mesma data.");
                return Page();
            }

            pacote.CapacityReached += msg => Console.WriteLine(msg);
            pacote.VerificarCapacidade();

            _context.Reservas.Add(Reserva);
            await _context.SaveChangesAsync();

            Action<string> log = null!;
            log += Logger.LogToConsole;
            log += Logger.LogToFile;
            log += Logger.LogToMemory;
            log($"Reserva criada para cliente {Reserva.ClienteId} no pacote {Reserva.PacoteTuristicoId} em {Reserva.DataReserva:dd/MM/yyyy}");

            // 3 - Uso de Func com Expressão Lambda
            Func<int, int, decimal> calcularTotal = (dias, diaria) => dias * diaria;
            int numeroDias = 3;
            int valorDiaria = 150;
            decimal valorTotal = calcularTotal(numeroDias, valorDiaria);
            Console.WriteLine($"Valor total estimado da reserva: R$ {valorTotal}");

            return RedirectToPage("./IndexReserva");
        }
    }

    // 1 - Delegate para Cálculo de Descontos
    public delegate decimal CalculateDelegate(decimal valor);

    public static class DescontoService {
        public static decimal AplicarDesconto(decimal valor) {
            return valor * 0.9M;
        }
    }

    // 2 - Multicast Delegate para Registro de Logs
    public static class Logger {
        public static List<string> LogMemory = new();

        public static void LogToConsole(string message) {
            Console.WriteLine($"[Console] {message}");
        }

        public static void LogToFile(string message) {
            File.AppendAllText("logs.txt", $"[File] {message}{Environment.NewLine}");
        }

        public static void LogToMemory(string message) {
            LogMemory.Add($"[Memory] {message}");
        }
    }
}
