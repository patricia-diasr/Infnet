from typing import List, Tuple
import random
import time


def intersecao_arrays(array1: List[int], array2: List[int]) -> Tuple[List[int], int]:
    """
    Retorna os elementos em comum entre dois arrays utilizando uma hash table para garantir complexidade linear

    Args:
        array1 (List[int]): Primeiro array
        array2 (List[int]): Segundo array

    Returns:
        Tuple[List[int], int]:
            - Lista contendo os elementos em comum
            - Número total de acessos à hash table
    """

    acessos = 0
    tabela_hash = {}
    resultado = []

    for elemento in array1:
        acessos += 1
        tabela_hash[elemento] = True

    for elemento in array2:
        acessos += 1
        if elemento in tabela_hash:
            resultado.append(elemento)

    return resultado, acessos


tamanhos = [1000, 2500, 5000, 10000, 20000]

for tamanho in tamanhos:
    array1 = [random.randint(0, tamanho * 2) for _ in range(tamanho)]
    array2 = [random.randint(0, tamanho * 2) for _ in range(tamanho)]

    print(f"\n===== Teste com arrays de tamanho {tamanho} =====")

    inicio = time.perf_counter()
    intersecao, acessos = intersecao_arrays(array1, array2)
    fim = time.perf_counter()

    print(f"\nQuantidade de elementos em comum: {len(intersecao)}")
    print(f"Acessos à hash table: {acessos}")
    print(f"Tempo de execução: {fim - inicio:.6f} segundos")
