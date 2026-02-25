from typing import List
import random

def bubble_sort(lista: List[int]) -> List[int]:
    """
    Ordena os elementos de uma lista de números utilizando o algoritmo Bubble Sort

    O algoritmo percorre repetidamente a lista, comparando elementos adjacentes e trocando-os 
    quando estão fora de ordem. A cada iteração, o maior elemento da parte não ordenada é 
    posicionado corretamente ao final da lista

    Args:
        lista (List[int]): Lista contendo os números a serem ordenados

    Returns:
        List[int]: Lista ordenada em ordem crescente
    """
    
    n = len(lista)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista


for i in range (5):
    quantidade = random.randint(0, 20) 
    numeros_embaralhados = [random.randint(0, 100) for _ in range(quantidade)]

    print(f"\n===== Teste {i+1} =====")
    print("Números embaralhados:", numeros_embaralhados) 
    
    numeros_ordenados = bubble_sort(numeros_embaralhados) 
    print("Números ordenados:", numeros_ordenados)
