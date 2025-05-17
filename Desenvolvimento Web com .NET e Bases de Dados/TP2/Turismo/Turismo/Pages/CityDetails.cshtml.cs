using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Turismo.Pages
{
    public class CityDetailsModel : PageModel
    {
        public string NomeCidade { get; set; }

        public void OnGet(string cityName) {
            NomeCidade = cityName;
        }
    }
}
