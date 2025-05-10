using Ex12.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Ex12.Pages {
    public class IndexModel : PageModel {
        private readonly ILogger<IndexModel> _logger;

        public IndexModel(ILogger<IndexModel> logger) {
            _logger = logger;

            OnEventoCriado = eventDetails => {
                _logger.LogInformation($"Evento Criado: {eventDetails.Titulo} em {eventDetails.Data} no local {eventDetails.Local}");
            };
        }

        public Action<Event> OnEventoCriado;

        [BindProperty]
        public Event Evento { get; set; }

        public bool EventoCriado { get; set; }

        public void OnGet() {
        }

        public void OnPost() {
            if (ModelState.IsValid) {
                EventoCriado = true;

                OnEventoCriado?.Invoke(Evento);
            }
        }
    }
}
