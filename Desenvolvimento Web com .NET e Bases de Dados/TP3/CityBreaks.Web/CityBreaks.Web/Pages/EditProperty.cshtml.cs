using CityBreaks.Web.Data;
using CityBreaks.Web.Models.ViewModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CityBreaks.Web.Pages {
    public class EditPropertyModel : PageModel {
        private readonly CityBreaksContext _context;

        public EditPropertyModel(CityBreaksContext context) {
            _context = context;
        }

        [BindProperty]
        public EditPropertyViewModel PropertyInput { get; set; }

        public List<SelectListItem> CitiesSelectList { get; set; }

        public async Task<IActionResult> OnGetAsync(int? id) {
            if (id == null)
                return NotFound();

            var property = await _context.Properties.FindAsync(id);

            if (property == null)
                return NotFound();

            PropertyInput = new EditPropertyViewModel {
                Name = property.Name,
                PricePerNight = property.PricePerNight,
                CityId = property.CityId
            };

            await LoadCitiesAsync();

            return Page();
        }

        public async Task<IActionResult> OnPostAsync(int? id) {
            if (id == null)
                return NotFound();

            if (!ModelState.IsValid) {
                await LoadCitiesAsync();
                return Page();
            }

            var propertyToUpdate = await _context.Properties.FindAsync(id);

            if (propertyToUpdate == null)
                return NotFound();

            propertyToUpdate.Name = PropertyInput.Name;
            propertyToUpdate.PricePerNight = PropertyInput.PricePerNight;
            propertyToUpdate.CityId = PropertyInput.CityId;

            await _context.SaveChangesAsync();

            return RedirectToPage("Cities");
        }

        private async Task LoadCitiesAsync() {
            var cities = await _context.Cities.ToListAsync();

            CitiesSelectList = new List<SelectListItem>();

            foreach (var city in cities) {
                CitiesSelectList.Add(new SelectListItem {
                    Value = city.Id.ToString(),
                    Text = city.Name
                });
            }
        }
    }
}
