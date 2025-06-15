using Microsoft.EntityFrameworkCore;
using SistemaTurismo.Models;

// 9 - Criação de DbContext
namespace SistemaTurismo.Data {
    public class SistemaTurismoContext : DbContext {

        public SistemaTurismoContext(DbContextOptions<SistemaTurismoContext> options) : base(options) {
        }

        public DbSet<Cliente> Clientes { get; set; }
        public DbSet<Reserva> Reservas { get; set; }
        public DbSet<PacoteTuristico> PacotesTuristicos { get; set; }
        public DbSet<Destino> Destinos { get; set; }
        public DbSet<PacoteTuristicoDestino> PacoteTuristicoDestinos { get; set; }

        // 10 - Modelagem e Relacionamento entre Entidades
        protected override void OnModelCreating(ModelBuilder modelBuilder) {
            modelBuilder.Entity<Reserva>()
                .HasOne(r => r.Cliente)
                .WithMany(c => c.Reservas)
                .HasForeignKey(r => r.ClienteId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Reserva>()
                .HasOne(r => r.PacoteTuristico)
                .WithMany(p => p.Reservas)
                .HasForeignKey(r => r.PacoteTuristicoId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<PacoteTuristicoDestino>()
                .HasKey(pd => new { pd.PacoteTuristicoId, pd.DestinoId });

            modelBuilder.Entity<PacoteTuristicoDestino>()
                .HasOne(pd => pd.PacoteTuristico)
                .WithMany(p => p.Destinos)
                .HasForeignKey(pd => pd.PacoteTuristicoId);

            modelBuilder.Entity<PacoteTuristicoDestino>()
                .HasOne(pd => pd.Destino)
                .WithMany(d => d.PacotesTuristicos)
                .HasForeignKey(pd => pd.DestinoId);
        }

    }
}
