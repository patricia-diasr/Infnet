from typing import List, Tuple
import time


def primeiro_valor_duplicado(lista: List[str]) -> Tuple[str, int]:
    """
    Retorna o primeiro valor duplicado encontrado em um array de strings, considerando que existe exatamente um par duplicado

    Args:
        lista (List[str]): Lista de strings

    Returns:
        Tuple[str, int]:
            - Primeiro valor duplicado encontrado
            - Número total de acessos à hash table
    """

    acessos = 0
    elementos_vistos = {}

    for elemento in lista:
        acessos += 1
        if elemento in elementos_vistos:
            return elemento, acessos
        else:
            elementos_vistos[elemento] = True

    return None, acessos  


testes = [
    ["x", "y", "z", "x"],
    ["maçã", "banana", "uva", "pera", "banana"],
    ["alpha", "beta", "gamma", "delta", "gamma"],
    ["dó", "ré", "mi", "fá", "sol", "lá", "si", "dó"],
    ["azul", "amarelo", "vermelho", "vermelho", "verde"],
    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "p", "v", "w", "x", "y", "z"]
]


for i, lista in enumerate(testes):
    print(f"\n===== Teste {i+1} =====")
    print("\nLista:", lista)

    inicio = time.perf_counter()
    duplicado, acessos = primeiro_valor_duplicado(lista)
    fim = time.perf_counter()

    print("Primeiro duplicado:", duplicado)
    print("Acessos à hash table:", acessos)
    print("Tamanho do lista:", len(lista))
    print(f"Tempo de execução: {fim - inicio:.6f} segundos\n")
