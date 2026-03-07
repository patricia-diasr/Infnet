from typing import List, Tuple
import random
import time


def particionar(lista: List[int], inicio: int, fim: int, contadores: dict) -> int:
    """
    Realiza o particionamento do QuickSort contando comparações e cópias

    Args:
        lista (List[int]): Lista a ser organizada
        inicio (int): Índice inicial
        fim (int): Índice final
        contadores (dict): Dicionário com contadores de operações

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
    QuickSort recursivo instrumentado

    Args:
        lista (List[int]): Lista a ser ordenada
        inicio (int): Índice inicial
        fim (int): Índice final
        contadores (dict): Estrutura para registrar operações
    """

    if inicio < fim:
        posicao_pivo = particionar(lista, inicio, fim, contadores)
        quicksort(lista, inicio, posicao_pivo - 1, contadores)
        quicksort(lista, posicao_pivo + 1, fim, contadores)


tamanhos = [10, 25, 50]
print("\n" + "=" * 40 + "\n")

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
    print(f"Testes com {tamanho} elementos")

    for nome, lista in cenarios.items():
        lista_copia = lista.copy()

        contadores = {
            "comparacoes": 0,
            "copias": 0
        }

        print(f"\nCenário: {nome}")
        print("Lista antes:", lista_copia)

        inicio = time.perf_counter()
        quicksort(lista_copia, 0, len(lista_copia) - 1, contadores)
        fim = time.perf_counter()

        print("Lista depois:", lista_copia)
        print("Comparações:", contadores["comparacoes"])
        print("Cópias:", contadores["copias"])
        print(f"Tempo de execução: {fim - inicio:.6f} segundos")

    print("\n" + "=" * 40 + "\n")
