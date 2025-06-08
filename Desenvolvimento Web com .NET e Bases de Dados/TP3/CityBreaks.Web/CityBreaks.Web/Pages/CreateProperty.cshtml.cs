using CityBreaks.Web.Data;
using CityBreaks.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using CityBreaks.Web.Models.ViewModels;


namespace CityBreaks.Web.Pages
{
    public class CreatePropertyModel : PageModel
    {
        private readonly CityBreaksContext _context;

        public CreatePropertyModel(CityBreaksContext context) {
            _context = context;
        }

        [BindProperty]
        public CreatePropertyViewModel PropertyInput { get; set; }

        public List<SelectListItem> CitiesSelectList { get; set; }

        public async Task OnGetAsync() {
            var cities = await _context.Cities.ToListAsync();

            CitiesSelectList = new List<SelectListItem>();

            foreach (var city in cities) {
                CitiesSelectList.Add(new SelectListItem {
                    Value = city.Id.ToString(),
                    Text = city.Name
                });
            }
        }

        public async Task<IActionResult> OnPostAsync() {
            if (!ModelState.IsValid) {
                await OnGetAsync();
                return Page();
            }

            var property = new Property {
                Name = PropertyInput.Name,
                PricePerNight = PropertyInput.PricePerNight,
                CityId = PropertyInput.CityId
            };

            await _context.Properties.AddAsync(property);
            await _context.SaveChangesAsync();

            return RedirectToPage("Cities");
        }
    }
}
