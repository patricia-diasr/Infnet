namespace EX6 {
    internal class Program {
        static void Main(string[] args) {
            Console.Write("Digite seu peso em kg: ");
            float peso = float.Parse(Console.ReadLine());

            Console.Write("Digite sua altura em metros: ");
            float altura = float.Parse(Console.ReadLine());

            float imc = peso / (altura * altura);
            string classificacao = "";

            if (imc < 18.5f) {
                classificacao = "Abaixo do peso";
            } 
            
            else if (imc >= 18.5f && imc < 24.9f) {
                classificacao = "Peso normal";
            } 
            
            else if (imc >= 25f && imc < 29.9f) {
                classificacao = "Sobrepeso";
            } 
            
            else if (imc >= 30f && imc < 34.9f) {
                classificacao = "Obesidade grau 1";
            } 
            
            else if (imc >= 35f && imc < 39.9f) {
                classificacao = "Obesidade grau 2";
            } 
            
            else {
                classificacao = "Obesidade grau 3 (mórbida)";
            }

            Console.WriteLine($"\nSeu IMC é: {imc:F2}");
            Console.WriteLine($"Sua classificação é: {classificacao}");
        }
    }
}
