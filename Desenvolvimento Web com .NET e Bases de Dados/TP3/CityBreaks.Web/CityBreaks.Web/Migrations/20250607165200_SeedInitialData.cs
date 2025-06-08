using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace CityBreaks.Web.Migrations
{
    /// <inheritdoc />
    public partial class SeedInitialData : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.InsertData(
                table: "Countries",
                columns: new[] { "id", "codigo", "nome" },
                values: new object[,]
                {
                    { 1, "BR", "Brasil" },
                    { 2, "FR", "França" },
                    { 3, "CA", "Canadá" },
                    { 4, "IT", "Itália" }
                });

            migrationBuilder.InsertData(
                table: "Cities",
                columns: new[] { "id", "pais_id", "nome" },
                values: new object[,]
                {
                    { 1, 1, "Rio de Janeiro" },
                    { 2, 2, "Paris" },
                    { 3, 3, "Toronto" },
                    { 4, 4, "Roma" }
                });

            migrationBuilder.InsertData(
                table: "Properties",
                columns: new[] { "id", "cidade_id", "nome", "preco_diaria" },
                values: new object[,]
                {
                    { 1, 1, "Apartamento Copacabana", 300.00m },
                    { 2, 2, "Flat na Champs-Élysées", 550.00m },
                    { 3, 3, "Condo no centro de Toronto", 450.00m },
                    { 4, 4, "Hotel perto do Coliseu", 450.00m }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 2);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 3);

            migrationBuilder.DeleteData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 4);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 2);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 3);

            migrationBuilder.DeleteData(
                table: "Cities",
                keyColumn: "id",
                keyValue: 4);

            migrationBuilder.DeleteData(
                table: "Countries",
                keyColumn: "id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Countries",
                keyColumn: "id",
                keyValue: 2);

            migrationBuilder.DeleteData(
                table: "Countries",
                keyColumn: "id",
                keyValue: 3);

            migrationBuilder.DeleteData(
                table: "Countries",
                keyColumn: "id",
                keyValue: 4);
        }
    }
}
