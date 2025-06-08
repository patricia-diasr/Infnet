using CityBreaks.Web.Models;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Data.Configurations {
    public class CountryConfiguration : IEntityTypeConfiguration<Country> {
        public void Configure(EntityTypeBuilder<Country> builder) {

            builder.Property(c => c.Id)
                    .HasColumnName("id");

            builder.Property(c => c.CountryName)
                   .HasMaxLength(100)
                   .HasColumnName("nome");

            builder.Property(c => c.CountryCode)
                   .HasMaxLength(10)
                   .HasColumnName("codigo");

            builder.HasData(
                new Country { Id = 1, CountryCode = "BR", CountryName = "Brasil" },
                new Country { Id = 2, CountryCode = "FR", CountryName = "França" },
                new Country { Id = 3, CountryCode = "CA", CountryName = "Canadá" },
                new Country { Id = 4, CountryCode = "IT", CountryName = "Itália" }
            );
        }
    }
}
