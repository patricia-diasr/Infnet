using CityBreaks.Web.Models;
using CityBreaks.Web.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CityBreaks.Web.Pages
{
    public class CitiesModel : PageModel
    {
        private readonly ICityService _cityService;

        public CitiesModel(ICityService cityService) {
            _cityService = cityService;
        }

        public List<City> Cities { get; set; }

        public async Task OnGetAsync() {
            Cities = await _cityService.GetAllAsync();
        }
    }
}
