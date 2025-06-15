using System.ComponentModel.DataAnnotations.Schema;

namespace SistemaTurismo.Models {
    public class PacoteTuristicoDestino {

        public int PacoteTuristicoId { get; set; }

        public PacoteTuristico PacoteTuristico { get; set; }

        public int DestinoId { get; set; }
        
        public Destino Destino { get; set; }
    }
}
