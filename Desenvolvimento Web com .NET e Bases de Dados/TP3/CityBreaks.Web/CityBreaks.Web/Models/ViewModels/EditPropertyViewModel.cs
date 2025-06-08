namespace CityBreaks.Web.Models.ViewModels {
    public class EditPropertyViewModel {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal PricePerNight { get; set; }
        public int CityId { get; set; }
    }
}
