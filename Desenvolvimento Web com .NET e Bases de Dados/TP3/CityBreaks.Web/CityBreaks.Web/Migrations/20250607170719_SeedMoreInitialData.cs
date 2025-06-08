using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace CityBreaks.Web.Migrations
{
    /// <inheritdoc />
    public partial class SeedMoreInitialData : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 2,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 1, "São Paulo" });

            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 3,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 1, "Salvador" });

            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 4,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 2, "Paris" });

            migrationBuilder.InsertData(
                table: "Cities",
                columns: new[] { "id", "pais_id", "nome" },
                values: new object[,]
                {
                    { 5, 2, "Lyon" },
                    { 6, 2, "Nice" },
                    { 7, 3, "Toronto" },
                    { 8, 3, "Vancouver" },
                    { 9, 3, "Montreal" },
                    { 10, 4, "Roma" },
                    { 11, 4, "Milão" },
                    { 12, 4, "Veneza" }
                });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 2,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 1, "Casa em Ipanema", 400.00m });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 3,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 1, "Studio em Botafogo", 250.00m });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 4,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 2, "Flat na Av. Paulista", 350.00m });

            migrationBuilder.InsertData(
                table: "Properties",
                columns: new[] { "id", "cidade_id", "nome", "preco_diaria" },
                values: new object[,]
                {
                    { 5, 2, "Apartamento Jardins", 450.00m },
                    { 6, 2, "Loft Vila Madalena", 300.00m },
                    { 7, 3, "Apartamento Pelourinho", 200.00m },
                    { 8, 3, "Casa Praia do Forte", 500.00m },
                    { 9, 3, "Pousada Barra", 250.00m },
                    { 10, 4, "Flat na Champs-Élysées", 550.00m },
                    { 11, 4, "Apartamento Montmartre", 500.00m },
                    { 12, 4, "Studio Torre Eiffel", 600.00m },
                    { 13, 5, "Apartamento Presqu'île", 400.00m },
                    { 14, 5, "Loft Croix-Rousse", 350.00m },
                    { 15, 5, "Studio Vieux Lyon", 300.00m },
                    { 16, 6, "Apartamento Promenade des Anglais", 450.00m },
                    { 17, 6, "Villa Côte d'Azur", 1000.00m },
                    { 18, 6, "Studio Centro Histórico", 350.00m },
                    { 19, 7, "Condo no centro de Toronto", 450.00m },
                    { 20, 7, "Apartamento Distillery District", 500.00m },
                    { 21, 7, "Loft Queen Street", 400.00m },
                    { 22, 8, "Apartamento Coal Harbour", 600.00m },
                    { 23, 8, "Casa Kitsilano", 700.00m },
                    { 24, 8, "Studio Gastown", 350.00m },
                    { 25, 9, "Apartamento Vieux-Montréal", 400.00m },
                    { 26, 9, "Loft Plateau Mont-Royal", 350.00m },
                    { 27, 9, "Studio Quartier Latin", 300.00m },
                    { 28, 10, "Hotel perto do Coliseu", 450.00m },
                    { 29, 10, "Apartamento Trastevere", 400.00m },
                    { 30, 10, "Studio Fontana di Trevi", 500.00m },
                    { 31, 11, "Apartamento Quadrilátero da Moda", 600.00m },
                    { 32, 11, "Loft Navigli", 500.00m },
                    { 33, 11, "Studio Duomo", 550.00m },
                    { 34, 12, "Apartamento perto da Praça de São Marcos", 500.00m },
                    { 35, 12, "Casa Canal Grande", 800.00m },
                    { 36, 12, "Studio Rialto", 450.00m }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 5);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 6);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 7);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 8);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 9);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 10);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 11);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 12);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 13);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 14);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 15);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 16);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 17);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 18);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 19);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 20);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 21);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 22);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 23);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 24);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 25);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 26);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 27);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 28);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 29);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 30);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 31);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 32);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 33);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 34);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 35);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 36);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 5);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 6);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 7);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 8);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 9);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 10);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 11);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 12);

            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 2,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 2, "Paris" });

            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 3,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 3, "Toronto" });

            migrationBuilder.UpdateData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 4,
                columns: new[] { "pais_id", "nome" },
                values: new object[] { 4, "Roma" });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 2,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 2, "Flat na Champs-Élysées", 550.00m });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 3,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 3, "Condo no centro de Toronto", 450.00m });

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 4,
                columns: new[] { "cidade_id", "nome", "preco_diaria" },
                values: new object[] { 4, "Hotel perto do Coliseu", 450.00m });
        }
    }
}
