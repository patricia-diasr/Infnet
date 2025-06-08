using CityBreaks.Web.Data;
using CityBreaks.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Services {
    public class CityService : ICityService {

        private readonly CityBreaksContext _context;

        public CityService(CityBreaksContext context) {
            _context = context;
        }

        public async Task<List<City>> GetAllAsync() {
            return await _context.Cities
                .Include(c => c.Country)
                .Select(c => new City {
                    Id = c.Id,
                    Name = c.Name,
                    Country = c.Country,
                    Properties = c.Properties.Where(p => p.DeletedAt == null).ToList()
                })
                .ToListAsync();
        }

        public async Task<City> GetByNameAsync(string name) {
            return await _context.Cities
                .Include(c => c.Country)
                .Where(c => EF.Functions.Collate(c.Name, "NOCASE") == name)
                .Select(c => new City {
                    Id = c.Id,
                    Name = c.Name,
                    Country = c.Country,
                    Properties = c.Properties.Where(p => p.DeletedAt == null).ToList()
                })
                .FirstOrDefaultAsync();
        }
    }
}
