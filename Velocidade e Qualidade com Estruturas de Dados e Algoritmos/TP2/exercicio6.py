from typing import List, Tuple
import random
import time


def selection_sort(lista: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista utilizando o algoritmo Selection Sort

    Args:
        lista (List[int]): Lista de números a serem ordenados

    Returns:
        Tuple[List[int], int, int]:
            - Lista ordenada
            - Total de comparações
            - Total de trocas
    """

    comparacoes = 0
    trocas = 0
    n = len(lista)

    for i in range(n - 1):
        indice_menor = i

        for j in range(i + 1, n):
            comparacoes += 1
            if lista[j] < lista[indice_menor]:
                indice_menor = j

        if indice_menor != i:
            lista[i], lista[indice_menor] = lista[indice_menor], lista[i]
            trocas += 1

    return lista, comparacoes, trocas


tamanhos = [5, 10, 20, 50]

for tamanho in tamanhos:
    base = list(range(1, tamanho + 1))
    
    lista_ordenada = base.copy()
    lista_invertida = base[::-1]
    lista_aleatoria = base.copy()
    random.shuffle(lista_aleatoria)
    
    cenarios = {
        "Ordenada": lista_ordenada,
        "Invertida": lista_invertida,
        "Aleatória": lista_aleatoria
    }
    
    print(f"\n===== Testes com {tamanho} elementos =====")
    
    for nome, lista in cenarios.items():
        lista_copia = lista.copy()
    
        print(f"\nEstado inicial: {nome}")
        print("Lista antes:", lista_copia)
    
        inicio = time.perf_counter()
        ordenada, comparacoes, trocas = selection_sort(lista_copia)
        fim = time.perf_counter()
    
        print("Lista depois:", ordenada)
        print(f"Comparações: {comparacoes}")
        print(f"Trocas: {trocas}")
        print(f"Tempo: {fim - inicio:.6f} segundos\n")
        print("=" * 35)
