using CityBreaks.Web.Models;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Data.Configurations {
    public class CityConfiguration : IEntityTypeConfiguration<City> {
        public void Configure(EntityTypeBuilder<City> builder) {

            builder.Property(c => c.Id)
                    .HasColumnName("id");

            builder.Property(c => c.Name)
                   .HasMaxLength(100)
                   .HasColumnName("nome");

            builder.Property(c => c.CountryId)
                   .HasColumnName("pais_id");

            builder.HasData(
                new City { Id = 1, Name = "Rio de Janeiro", CountryId = 1 },
                new City { Id = 2, Name = "São Paulo", CountryId = 1 },
                new City { Id = 3, Name = "Salvador", CountryId = 1 },

                new City { Id = 4, Name = "Paris", CountryId = 2 },
                new City { Id = 5, Name = "Lyon", CountryId = 2 },
                new City { Id = 6, Name = "Nice", CountryId = 2 },

                new City { Id = 7, Name = "Toronto", CountryId = 3 },
                new City { Id = 8, Name = "Vancouver", CountryId = 3 },
                new City { Id = 9, Name = "Montreal", CountryId = 3 },

                new City { Id = 10, Name = "Roma", CountryId = 4 },
                new City { Id = 11, Name = "Milão", CountryId = 4 },
                new City { Id = 12, Name = "Veneza", CountryId = 4 }
            );
        }
    }
}
