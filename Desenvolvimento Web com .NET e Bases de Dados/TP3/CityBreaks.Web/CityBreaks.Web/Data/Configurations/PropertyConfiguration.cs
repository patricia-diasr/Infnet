using CityBreaks.Web.Models;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Data.Configurations {
    public class PropertyConfiguration : IEntityTypeConfiguration<Property> {
        public void Configure(EntityTypeBuilder<Property> builder) {

            builder.Property(p => p.Id)
                    .HasColumnName("id");

            builder.Property(p => p.Name)
                   .HasMaxLength(150)
                   .HasColumnName("nome");

            builder.Property(p => p.PricePerNight)
                   .HasColumnName("preco_diaria");

            builder.Property(p => p.CityId)
                   .HasColumnName("cidade_id");

            builder.HasData(
                new Property { Id = 1, Name = "Apartamento Copacabana", PricePerNight = 300.00m, CityId = 1 },
                new Property { Id = 2, Name = "Casa em Ipanema", PricePerNight = 400.00m, CityId = 1 },
                new Property { Id = 3, Name = "Studio em Botafogo", PricePerNight = 250.00m, CityId = 1 },

                new Property { Id = 4, Name = "Flat na Av. Paulista", PricePerNight = 350.00m, CityId = 2 },
                new Property { Id = 5, Name = "Apartamento Jardins", PricePerNight = 450.00m, CityId = 2 },
                new Property { Id = 6, Name = "Loft Vila Madalena", PricePerNight = 300.00m, CityId = 2 },

                new Property { Id = 7, Name = "Apartamento Pelourinho", PricePerNight = 200.00m, CityId = 3 },
                new Property { Id = 8, Name = "Casa Praia do Forte", PricePerNight = 500.00m, CityId = 3 },
                new Property { Id = 9, Name = "Pousada Barra", PricePerNight = 250.00m, CityId = 3 },

                new Property { Id = 10, Name = "Flat na Champs-Élysées", PricePerNight = 550.00m, CityId = 4 },
                new Property { Id = 11, Name = "Apartamento Montmartre", PricePerNight = 500.00m, CityId = 4 },
                new Property { Id = 12, Name = "Studio Torre Eiffel", PricePerNight = 600.00m, CityId = 4 },

                new Property { Id = 13, Name = "Apartamento Presqu'île", PricePerNight = 400.00m, CityId = 5 },
                new Property { Id = 14, Name = "Loft Croix-Rousse", PricePerNight = 350.00m, CityId = 5 },
                new Property { Id = 15, Name = "Studio Vieux Lyon", PricePerNight = 300.00m, CityId = 5 },

                new Property { Id = 16, Name = "Apartamento Promenade des Anglais", PricePerNight = 450.00m, CityId = 6 },
                new Property { Id = 17, Name = "Villa Côte d'Azur", PricePerNight = 1000.00m, CityId = 6 },
                new Property { Id = 18, Name = "Studio Centro Histórico", PricePerNight = 350.00m, CityId = 6 },

                new Property { Id = 19, Name = "Condo no centro de Toronto", PricePerNight = 450.00m, CityId = 7 },
                new Property { Id = 20, Name = "Apartamento Distillery District", PricePerNight = 500.00m, CityId = 7 },
                new Property { Id = 21, Name = "Loft Queen Street", PricePerNight = 400.00m, CityId = 7 },

                new Property { Id = 22, Name = "Apartamento Coal Harbour", PricePerNight = 600.00m, CityId = 8 },
                new Property { Id = 23, Name = "Casa Kitsilano", PricePerNight = 700.00m, CityId = 8 },
                new Property { Id = 24, Name = "Studio Gastown", PricePerNight = 350.00m, CityId = 8 },

                new Property { Id = 25, Name = "Apartamento Vieux-Montréal", PricePerNight = 400.00m, CityId = 9 },
                new Property { Id = 26, Name = "Loft Plateau Mont-Royal", PricePerNight = 350.00m, CityId = 9 },
                new Property { Id = 27, Name = "Studio Quartier Latin", PricePerNight = 300.00m, CityId = 9 },

                new Property { Id = 28, Name = "Hotel perto do Coliseu", PricePerNight = 450.00m, CityId = 10 },
                new Property { Id = 29, Name = "Apartamento Trastevere", PricePerNight = 400.00m, CityId = 10 },
                new Property { Id = 30, Name = "Studio Fontana di Trevi", PricePerNight = 500.00m, CityId = 10 },

                new Property { Id = 31, Name = "Apartamento Quadrilátero da Moda", PricePerNight = 600.00m, CityId = 11 },
                new Property { Id = 32, Name = "Loft Navigli", PricePerNight = 500.00m, CityId = 11 },
                new Property { Id = 33, Name = "Studio Duomo", PricePerNight = 550.00m, CityId = 11 },

                new Property { Id = 34, Name = "Apartamento perto da Praça de São Marcos", PricePerNight = 500.00m, CityId = 12 },
                new Property { Id = 35, Name = "Casa Canal Grande", PricePerNight = 800.00m, CityId = 12 },
                new Property { Id = 36, Name = "Studio Rialto", PricePerNight = 450.00m, CityId = 12 }
            );
        }
    }
}
