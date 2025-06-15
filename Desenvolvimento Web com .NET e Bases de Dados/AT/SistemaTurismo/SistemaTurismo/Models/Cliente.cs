using System.ComponentModel.DataAnnotations;

namespace SistemaTurismo.Models {
    public class Cliente {

        public int Id { get; set; }

        [Required(ErrorMessage = "O nome é obrigatório.")]
        [MinLength(3, ErrorMessage = "O nome deve ter pelo menos 3 caracteres.")]
        [StringLength(100, ErrorMessage = "O nome pode ter no máximo 100 caracteres.")]
        public string Nome { get; set; }

        [Required(ErrorMessage = "O e-mail é obrigatório.")]
        [EmailAddress(ErrorMessage = "E-mail inválido.")]
        public string Email { get; set; }

        public List<Reserva> Reservas { get; set; } = new List<Reserva>();

        public DateTime? DeletedAt { get; set; }
    }
}
