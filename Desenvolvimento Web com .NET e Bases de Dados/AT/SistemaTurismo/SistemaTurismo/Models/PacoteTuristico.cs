using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel;

namespace SistemaTurismo.Models {
    public class PacoteTuristico {

        public int Id { get; set; }

        [Required(ErrorMessage = "O título é obrigatório.")]
        [MinLength(5, ErrorMessage = "O título deve ter pelo menos 5 caracteres.")]
        public string Titulo { get; set; }

        [Required(ErrorMessage = "A data de início é obrigatória.")]
        public DateTime DataInicio { get; set; }

        [Range(1, 1000, ErrorMessage = "A capacidade deve ser entre 1 e 1000.")]
        public int CapacidadeMaxima { get; set; }

        [Required(ErrorMessage = "O preço é obrigatório.")]
        [Range(0.01, 100000, ErrorMessage = "O preço deve ser maior que 0.")]
        [Column(TypeName = "decimal(10,2)")]
        public decimal Preco { get; set; }

        public List<PacoteTuristicoDestino> Destinos { get; set; } = new List<PacoteTuristicoDestino>();

        public List<Reserva> Reservas { get; set; } = new List<Reserva>();

        public DateTime? DeletedAt { get; set; }

        public event Action<string>? CapacityReached;

        // 4 - Evento de Alerta para Limite de Capacidade
        public void VerificarCapacidade() {
            int ativos = Reservas.Count(r => r.DeletedAt == null);
            if (ativos >= CapacidadeMaxima) {
                CapacityReached?.Invoke($"Capacidade atingida para o pacote '{Titulo}'!");
            }
        }
    }
}
