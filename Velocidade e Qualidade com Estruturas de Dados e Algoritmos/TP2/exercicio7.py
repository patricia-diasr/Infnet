from typing import List, Tuple
import random
import time


def insertion_sort(lista: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista utilizando o algoritmo Insertion Sort

    Args:
        lista (List[int]): Lista de números a serem ordenados

    Returns:
        Tuple[List[int], int, int]:
            - Lista ordenada
            - Total de comparações
            - Total de deslocamentos
    """

    comparacoes = 0
    deslocamentos = 0

    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1

        while j >= 0:
            comparacoes += 1
            if lista[j] > chave:
                lista[j + 1] = lista[j]
                deslocamentos += 1
                j -= 1
            else:
                break

        lista[j + 1] = chave

    return lista, comparacoes, deslocamentos


tamanhos = [5, 10, 20, 50]

for tamanho in tamanhos:
    base = list(range(1, tamanho + 1))

    lista_ordenada = base.copy()
    lista_quase_ordenada = base.copy()
    lista_quase_ordenada[-1], lista_quase_ordenada[-2] = (
        lista_quase_ordenada[-2],
        lista_quase_ordenada[-1],
    )
    lista_invertida = base[::-1]
    lista_aleatoria = base.copy()
    random.shuffle(lista_aleatoria)

    cenarios = {
        "Ordenada": lista_ordenada,
        "Quase Ordenada": lista_quase_ordenada,
        "Invertida": lista_invertida,
        "Aleatória": lista_aleatoria
    }

    print(f"\n===== Testes com {tamanho} elementos =====")

    for nome, lista in cenarios.items():
        lista_copia = lista.copy()

        print(f"\nEstado inicial: {nome}")
        print("Lista antes:", lista_copia)

        inicio = time.perf_counter()
        ordenada, comparacoes, deslocamentos = insertion_sort(lista_copia)
        fim = time.perf_counter()

        print("Lista depois:", ordenada)
        print(f"Comparações: {comparacoes}")
        print(f"Deslocamentos: {deslocamentos}")
        print(f"Tempo: {fim - inicio:.6f} segundos\n")
        print("=" * 35)
