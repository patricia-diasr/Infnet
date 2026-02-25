from typing import Tuple
import string
import time


def letra_ausente(texto: str) -> Tuple[str, int]:
    """
    Identifica a letra ausente do alfabeto em uma string, considerando apenas caracteres de 'a' a 'z'

    Ignora letras maiúsculas, espaços, números e pontuação

    Args:
        texto (str): Texto a ser analisado

    Returns:
        Tuple[str, int]:
            - Letra ausente do alfabeto (ou None se nenhuma estiver ausente)
            - Número total de acessos à estrutura auxiliar
    """

    acessos = 0
    letras_presentes = {}

    for caractere in texto.lower():
        if 'a' <= caractere <= 'z':
            acessos += 1
            letras_presentes[caractere] = True

    for letra in string.ascii_lowercase:
        acessos += 1
        if letra not in letras_presentes:
            return letra, acessos

    return None, acessos


textos= [
    "Velocidade e Qualidade com Estruturas de Dados e Algoritmos",
    "abcdefghijklmnopqrstuvwxyz",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
]

for i, texto in enumerate(textos):
    print(f"\n===== Teste {i+1} =====")
    print("Texto:", texto)

    inicio = time.perf_counter()
    ausente, acessos = letra_ausente(texto)
    fim = time.perf_counter()

    print("Letra ausente:", ausente)
    print("Tamanho do texto:", len(texto))
    print("Acessos à estrutura:", acessos)
    print(f"Tempo de execução: {fim - inicio:.6f} segundos")
