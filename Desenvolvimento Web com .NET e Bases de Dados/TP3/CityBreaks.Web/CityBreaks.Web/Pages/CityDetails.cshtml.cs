using CityBreaks.Web.Models;
using CityBreaks.Web.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace CityBreaks.Web.Pages
{
    public class CityDetailsModel : PageModel
    {
        private readonly ICityService _cityService;

        private readonly IPropertyService _propertyService;


        public CityDetailsModel(ICityService cityService, IPropertyService propertyService) {
            _cityService = cityService;
            _propertyService = propertyService;
        }

        public City City { get; set; }

        public async Task<IActionResult> OnGetAsync(string name) {
            if (string.IsNullOrEmpty(name)) {
                return NotFound();
            }

            City = await _cityService.GetByNameAsync(name);

            if (City == null) {
                return NotFound();
            }

            return Page();
        }

        public async Task<IActionResult> OnPostDeleteAsync(int id) {
            await _propertyService.DeleteAsync(id);
            return RedirectToPage("Cities");
        }
    }
}
