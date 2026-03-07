from typing import List
import random


def particionar(lista: List[int], inicio: int, fim: int, contadores: dict) -> int:
    """
    Particionamento utilizado tanto no QuickSort quanto no QuickSelect

    Args:
        lista (List[int]): Lista de números
        inicio (int): Índice inicial
        fim (int): Índice final
        contadores (dict): Contadores de operações

    Returns:
        int: Índice final do pivô
    """

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        contadores["comparacoes"] += 1

        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
            contadores["copias"] += 3

    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
    contadores["copias"] += 3

    return i + 1


def quicksort(lista: List[int], inicio: int, fim: int, contadores: dict) -> None:
    """
    Ordena uma lista utilizando o algoritmo QuickSort recursivo instrumentado

    Args:
        lista (List[int]): Lista de números a ser ordenada
        inicio (int): Índice inicial da partição a ser processada
        fim (int): Índice final da partição a ser processada
        contadores (dict): Dicionário utilizado para registrar o número de comparações e cópias realizadas durante a execução

    Returns:
        None: A lista é modificada diretamente (in-place)
    """

    if inicio < fim:
        p = particionar(lista, inicio, fim, contadores)

        quicksort(lista, inicio, p - 1, contadores)
        quicksort(lista, p + 1, fim, contadores)


def quickselect(lista: List[int], inicio: int, fim: int, k: int, contadores: dict) -> int:
    """
    Encontra o elemento que estaria na posição k se a lista estivesse ordenada, utilizando o algoritmo QuickSelect

    Args:
        lista (List[int]): Lista de números
        inicio (int): Índice inicial da partição analisada
        fim (int): Índice final da partição analisada
        k (int): Índice do elemento desejado na ordem crescente
        contadores (dict): Dicionário utilizado para registrar o número de comparações e cópias realizadas durante a execução

    Returns:
        int: Valor do elemento que ocupa a posição k na lista ordenada
    """

    if inicio <= fim:
        p = particionar(lista, inicio, fim, contadores)

        if p == k:
            return lista[p]

        elif k < p:
            return quickselect(lista, inicio, p - 1, k, contadores)

        else:
            return quickselect(lista, p + 1, fim, k, contadores)


tamanhos = [10, 25, 50]
print("\n" + "=" * 40 + "\n")

for tamanho in tamanhos:
    base = list(range(1, tamanho + 1))
    random.shuffle(base)

    lista_quicksort = base.copy()
    lista_quickselect = base.copy()

    indice_mediana = len(base) // 2

    print(f"Testes com {tamanho} elementos")
    print("Lista original:", base)

    contadores_qs = {"comparacoes": 0, "copias": 0}
    quicksort(lista_quicksort, 0, len(lista_quicksort) - 1, contadores_qs)

    print("\nQuickSort:")
    print("Lista ordenada:", lista_quicksort)
    print("Comparações:", contadores_qs["comparacoes"])
    print("Cópias:", contadores_qs["copias"])

    contadores_qsel = {"comparacoes": 0, "copias": 0}
    mediana = quickselect(
        lista_quickselect,
        0,
        len(lista_quickselect) - 1,
        indice_mediana,
        contadores_qsel
    )

    print("\nQuickSelect:")
    print("Mediana encontrada:", mediana)
    print("Comparações:", contadores_qsel["comparacoes"])
    print("Cópias:", contadores_qsel["copias"])
    print("Índice da mediana:", indice_mediana)
    print("\n" + "=" * 40 + "\n")
