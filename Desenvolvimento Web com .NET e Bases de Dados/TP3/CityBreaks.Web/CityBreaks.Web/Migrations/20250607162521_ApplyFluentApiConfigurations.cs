using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace CityBreaks.Web.Migrations
{
    /// <inheritdoc />
    public partial class ApplyFluentApiConfigurations : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Cities_Countries_CountryId",
                table: "Cities");

            migrationBuilder.DropForeignKey(
                name: "FK_Properties_Cities_CityId",
                table: "Properties");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "Properties",
                newName: "id");

            migrationBuilder.RenameColumn(
                name: "PricePerNight",
                table: "Properties",
                newName: "preco_diaria");

            migrationBuilder.RenameColumn(
                name: "Name",
                table: "Properties",
                newName: "nome");

            migrationBuilder.RenameColumn(
                name: "CityId",
                table: "Properties",
                newName: "cidade_id");

            migrationBuilder.RenameIndex(
                name: "IX_Properties_CityId",
                table: "Properties",
                newName: "IX_Properties_cidade_id");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "Countries",
                newName: "id");

            migrationBuilder.RenameColumn(
                name: "CountryName",
                table: "Countries",
                newName: "nome");

            migrationBuilder.RenameColumn(
                name: "CountryCode",
                table: "Countries",
                newName: "codigo");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "Cities",
                newName: "id");

            migrationBuilder.RenameColumn(
                name: "Name",
                table: "Cities",
                newName: "nome");

            migrationBuilder.RenameColumn(
                name: "CountryId",
                table: "Cities",
                newName: "pais_id");

            migrationBuilder.RenameIndex(
                name: "IX_Cities_CountryId",
                table: "Cities",
                newName: "IX_Cities_pais_id");

            migrationBuilder.AddForeignKey(
                name: "FK_Cities_Countries_pais_id",
                table: "Cities",
                column: "pais_id",
                principalTable: "Countries",
                principalColumn: "id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Properties_Cities_cidade_id",
                table: "Properties",
                column: "cidade_id",
                principalTable: "Cities",
                principalColumn: "id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Cities_Countries_pais_id",
                table: "Cities");

            migrationBuilder.DropForeignKey(
                name: "FK_Properties_Cities_cidade_id",
                table: "Properties");

            migrationBuilder.RenameColumn(
                name: "id",
                table: "Properties",
                newName: "Id");

            migrationBuilder.RenameColumn(
                name: "preco_diaria",
                table: "Properties",
                newName: "PricePerNight");

            migrationBuilder.RenameColumn(
                name: "nome",
                table: "Properties",
                newName: "Name");

            migrationBuilder.RenameColumn(
                name: "cidade_id",
                table: "Properties",
                newName: "CityId");

            migrationBuilder.RenameIndex(
                name: "IX_Properties_cidade_id",
                table: "Properties",
                newName: "IX_Properties_CityId");

            migrationBuilder.RenameColumn(
                name: "id",
                table: "Countries",
                newName: "Id");

            migrationBuilder.RenameColumn(
                name: "nome",
                table: "Countries",
                newName: "CountryName");

            migrationBuilder.RenameColumn(
                name: "codigo",
                table: "Countries",
                newName: "CountryCode");

            migrationBuilder.RenameColumn(
                name: "id",
                table: "Cities",
                newName: "Id");

            migrationBuilder.RenameColumn(
                name: "pais_id",
                table: "Cities",
                newName: "CountryId");

            migrationBuilder.RenameColumn(
                name: "nome",
                table: "Cities",
                newName: "Name");

            migrationBuilder.RenameIndex(
                name: "IX_Cities_pais_id",
                table: "Cities",
                newName: "IX_Cities_CountryId");

            migrationBuilder.AddForeignKey(
                name: "FK_Cities_Countries_CountryId",
                table: "Cities",
                column: "CountryId",
                principalTable: "Countries",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Properties_Cities_CityId",
                table: "Properties",
                column: "CityId",
                principalTable: "Cities",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
