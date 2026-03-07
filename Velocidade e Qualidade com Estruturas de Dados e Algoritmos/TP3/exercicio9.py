from typing import List
import random
import time


def particionar(lista: List[int], inicio: int, fim: int) -> int:
    """
    Realiza o particionamento do QuickSort utilizando o último elemento como pivô

    Args:
        lista (List[int]): Lista a ser organizada
        inicio (int): Índice inicial da partição
        fim (int): Índice final da partição

    Returns:
        int: Índice final do pivô após o particionamento
    """

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]

    return i + 1


def quicksort(lista: List[int], inicio: int, fim: int) -> None:
    """
    Ordena uma lista utilizando o algoritmo QuickSort recursivo

    Args:
        lista (List[int]): Lista a ser ordenada
        inicio (int): Índice inicial
        fim (int): Índice final
    """

    if inicio < fim:
        posicao_pivo = particionar(lista, inicio, fim)
        quicksort(lista, inicio, posicao_pivo - 1)
        quicksort(lista, posicao_pivo + 1, fim)


tamanhos = [10, 25, 50]
print("\n" + "=" * 40 + "\n")

for tamanho in tamanhos:
    lista_ordenada = list(range(1, tamanho + 1))
    lista_invertida = lista_ordenada[::-1]

    lista_aleatoria = lista_ordenada.copy()
    random.shuffle(lista_aleatoria)

    cenarios = {
        "Ordenada": lista_ordenada,
        "Invertida": lista_invertida,
        "Aleatória": lista_aleatoria
    }

    print(f"Testes com {tamanho} elementos")

    for nome, lista in cenarios.items():
        lista_copia = lista.copy()

        print(f"\nEstado inicial: {nome}")
        print("Lista antes:", lista_copia)

        inicio = time.perf_counter()
        quicksort(lista_copia, 0, len(lista_copia) - 1)
        fim = time.perf_counter()

        print("Lista depois:", lista_copia)
        print(f"Tempo de execução: {fim - inicio:.6f} segundos")
    print("\n" + "=" * 40 + "\n")

