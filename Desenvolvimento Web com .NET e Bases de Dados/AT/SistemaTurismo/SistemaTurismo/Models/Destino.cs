using System.ComponentModel.DataAnnotations;

// 6 - Cadastro de Entidade com Objeto Complexo
namespace SistemaTurismo.Models {
    public class Destino {

        public int Id { get; set; }

        [Required(ErrorMessage = "O nome do destino é obrigatório.")]
        [MinLength(3, ErrorMessage = "O nome do destino deve ter pelo menos 3 caracteres.")]
        public string Nome { get; set; }

        [Required(ErrorMessage = "O país é obrigatório.")]
        [MinLength(2, ErrorMessage = "O nome do país deve ter pelo menos 2 caracteres.")]
        public string Pais { get; set; }

        public List<PacoteTuristicoDestino> PacotesTuristicos { get; set; } = new List<PacoteTuristicoDestino>();

        public DateTime? DeletedAt { get; set; }
    }
}
