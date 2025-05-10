using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace Ex8.Pages {
    public class IndexModel : PageModel {
        private readonly ILogger<IndexModel> _logger;

        public IndexModel(ILogger<IndexModel> logger) {
            _logger = logger;
        }

        public List<Produto> Produtos { get; set; }

        public void OnGet() {
            Produtos = new List<Produto>
            {
                new Produto { Nome = "Blusa", Preco = 49.90m },
                new Produto { Nome = "Tênis", Preco = 189.99m },
                new Produto { Nome = "Sandália", Preco = 149.00m }
            };
        }

        public class Produto {
            public string Nome { get; set; }
            public decimal Preco { get; set; }
        }
    }
}
