using CityBreaks.Web.Data;
using CityBreaks.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Services {
    public class PropertyService : IPropertyService {

        private readonly CityBreaksContext _context;

        public PropertyService(CityBreaksContext context) {
            _context = context;
        }

        public async Task DeleteAsync(int id) {
            var property = await _context.Properties.FindAsync(id);
            if (property == null)
                throw new ArgumentException("Propriedade não encontrada.");

            property.DeletedAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();
        }

        public async Task<List<Property>> GetFilteredAsync(decimal? minPrice, decimal? maxPrice, string cityName, string propertyName) {
            var query = _context.Properties
                .Include(p => p.City)
                .ThenInclude(c => c.Country)
                .Where(p => p.DeletedAt == null)
                .AsQueryable();

            if (minPrice.HasValue) {
                query = query.Where(p => p.PricePerNight >= minPrice.Value);
            }

            if (maxPrice.HasValue) {
                query = query.Where(p => p.PricePerNight <= maxPrice.Value);
            }

            if (!string.IsNullOrWhiteSpace(cityName)) {
                query = query.Where(p => EF.Functions.Like(p.City.Name, $"%{cityName}%"));
            }

            if (!string.IsNullOrWhiteSpace(propertyName)) {
                query = query.Where(p => EF.Functions.Like(p.Name, $"%{propertyName}%"));
            }

            return await query.ToListAsync();
        }

    }
}
