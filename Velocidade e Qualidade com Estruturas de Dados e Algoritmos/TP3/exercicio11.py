from typing import List
import random


def particionar(lista: List[int], inicio: int, fim: int) -> int:
    """
    Realiza o particionamento da lista utilizando o último elemento como pivô

    Args:
        lista (List[int]): Lista de números
        inicio (int): Índice inicial
        fim (int): Índice final

    Returns:
        int: Índice final do pivô
    """

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]

    return i + 1


def quickselect(lista: List[int], inicio: int, fim: int, k: int) -> int:
    """
    Encontra o elemento que estaria na posição k da lista ordenada

    Args:
        lista (List[int]): Lista de números
        inicio (int): Índice inicial
        fim (int): Índice final
        k (int): Índice desejado

    Returns:
        int: Elemento encontrado na posição k
    """

    if inicio <= fim:
        posicao_pivo = particionar(lista, inicio, fim)

        if posicao_pivo == k:
            return lista[posicao_pivo]

        elif k < posicao_pivo:
            return quickselect(lista, inicio, posicao_pivo - 1, k)

        else:
            return quickselect(lista, posicao_pivo + 1, fim, k)


testes = [
    [7, 2, 9, 4, 1, 6],
    [15, 3, 8, 10, 2, 6, 12],
    [20, 5, 1, 17, 9, 13, 11]
]
print("\n" + "=" * 40 + "\n")

for i, lista in enumerate(testes):
    lista_copia = lista.copy()
    indice_mediana = len(lista_copia) // 2

    print(f"Teste {i+1}")
    print("Lista original:", lista_copia)

    mediana = quickselect(lista_copia, 0, len(lista_copia) - 1, indice_mediana)

    print("Índice da mediana:", indice_mediana)
    print("Valor da mediana:", mediana)
    print("\n" + "=" * 40 + "\n")
