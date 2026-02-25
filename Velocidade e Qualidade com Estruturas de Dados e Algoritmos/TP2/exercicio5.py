from typing import Tuple
import time


def primeiro_caractere_nao_repetido(texto: str) -> Tuple[str, int]:
    """
    Retorna o primeiro caractere não repetido de uma string

    Args:
        texto (str): String a ser analisada

    Returns:
        Tuple[str, int]:
            - Primeiro caractere não repetido (ou None se não existir)
            - Número total de acessos à estrutura auxiliar
    """

    acessos = 0
    frequencias = {}

    for caractere in texto:
        acessos += 1
        if caractere in frequencias:
            frequencias[caractere] += 1
        else:
            frequencias[caractere] = 1

    for caractere in texto:
        acessos += 1
        if frequencias[caractere] == 1:
            return caractere, acessos

    return None, acessos


textos = [
    "velocidade e qualidade com estruturas de dados e algoritmos",
    "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxy",
    "lorem ipsum dolor sit amet, consectetur, adipiscing elit."
]

for i, texto in enumerate(textos):
    print(f"\n===== Teste {i+1} =====")
    print("Texto:", texto)

    inicio = time.perf_counter()
    caractere, acessos = primeiro_caractere_nao_repetido(texto)
    fim = time.perf_counter()

    print("Primeiro não repetido:", caractere)
    print("Tamanho do texto:", len(texto))
    print("Acessos à estrutura:", acessos)
    print(f"Tempo de execução: {fim - inicio:.6f} segundos")
