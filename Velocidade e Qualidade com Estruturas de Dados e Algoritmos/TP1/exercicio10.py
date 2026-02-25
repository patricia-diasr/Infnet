from typing import List

def bubble_sort_strings(lista: List[str]) -> List[str]:
    """
    Ordena os elementos de uma lista de strings em ordem alfabética utilizando o algoritmo 
    Bubble Sort

    Args:
        lista (List[str]): Lista contendo as strings a serem ordenadas

    Returns:
        List[str]: Lista de strings ordenadas em ordem alfabética
    """
    
    n = len(lista)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista


listas_strings = [
    ["banana", "maçã", "abacaxi", "uva"],
    ["Carlos", "ana", "Bruno"],
    ["z", "a", "m"],
    []
]

for i, lista in enumerate(listas_strings):
    print(f"\n===== Teste {i+1} =====")
    print("Lista original:", lista)
    print("Lista ordenada:", bubble_sort_strings(lista.copy()))
