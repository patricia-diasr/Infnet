using System.Globalization;
using System.Text;

namespace EX02 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite seu nome: ");
            String nome = Console.ReadLine();

            String nomeNormalizado = new string(nome.Normalize(NormalizationForm.FormD)
                    .ToCharArray()
                    .Where(c => CharUnicodeInfo.GetUnicodeCategory(c) != UnicodeCategory.NonSpacingMark)
                    .ToArray());
            String nomeCifrado = "";

            foreach (char letra in nomeNormalizado) {

                if (char.IsLetter(letra)) {
                    char letraInicio = char.IsUpper(letra) ? 'A' : 'a';
                    nomeCifrado += (char)(letraInicio + (letra - letraInicio + 2) % 26);
                }
                
                else {
                    nomeCifrado += letra;
                }
            }

            Console.WriteLine($"Nome cifrado: {nomeCifrado}");

        }
    }
}
