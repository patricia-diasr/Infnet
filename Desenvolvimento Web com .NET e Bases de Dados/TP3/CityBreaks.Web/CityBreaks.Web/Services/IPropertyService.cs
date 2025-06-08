using CityBreaks.Web.Models;

namespace CityBreaks.Web.Services {
    public interface IPropertyService {

        Task DeleteAsync(int id);

        Task<List<Property>> GetFilteredAsync(decimal? minPrice, decimal? maxPrice, string cityName, string propertyName);

    }
}
