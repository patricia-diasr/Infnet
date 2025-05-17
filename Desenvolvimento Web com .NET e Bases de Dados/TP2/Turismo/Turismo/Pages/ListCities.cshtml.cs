using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Turismo.Pages
{
    public class ListCitiesModel : PageModel
    {
        public List<string> Cidades { get; set; } = new List<string>
        {
            "Rio",
            "S�o Paulo",
            "Bras�lia"
        };

        public void OnGet() {
        }
    }
}
