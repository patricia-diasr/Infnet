using CityBreaks.Web.Models;

namespace CityBreaks.Web.Services {
    public interface ICityService {
        
        Task<List<City>> GetAllAsync();

        Task<City> GetByNameAsync(string name);
    }
}
