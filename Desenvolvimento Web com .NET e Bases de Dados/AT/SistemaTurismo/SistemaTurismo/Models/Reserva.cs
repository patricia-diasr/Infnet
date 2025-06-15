namespace SistemaTurismo.Models {
    public class Reserva {

        public int Id { get; set; }

        public int ClienteId { get; set; }

        public Cliente? Cliente { get; set; }

        public int PacoteTuristicoId { get; set; }

        public PacoteTuristico? PacoteTuristico { get; set; }

        public DateTime DataReserva { get; set; }

        public DateTime? DeletedAt { get; set; }
    }
}
