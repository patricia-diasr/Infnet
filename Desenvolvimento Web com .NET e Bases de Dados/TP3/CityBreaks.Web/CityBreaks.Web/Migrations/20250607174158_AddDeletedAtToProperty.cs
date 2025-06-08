using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace CityBreaks.Web.Migrations
{
    /// <inheritdoc />
    public partial class AddDeletedAtToProperty : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateTime>(
                name: "DeletedAt",
                table: "Properties",
                type: "TEXT",
                nullable: true);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 1,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 2,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 3,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 4,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 5,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 6,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 7,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 8,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 9,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 10,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 11,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 12,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 13,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 14,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 15,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 16,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 17,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 18,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 19,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 20,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 21,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 22,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 23,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 24,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 25,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 26,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 27,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 28,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 29,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 30,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 31,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 32,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 33,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 34,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 35,
                column: "DeletedAt",
                value: null);

            migrationBuilder.UpdateData(
                table: "Properties",
                keyColumn: "id",
                keyValue: 36,
                column: "DeletedAt",
                value: null);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "DeletedAt",
                table: "Properties");
        }
    }
}
