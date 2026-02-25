from typing import List

def greatest_number(array: List[int]) -> int:
    """
    Encontra o maior número em um array utilizando uma abordagem linear

    O algoritmo percorre o array uma única vez, mantendo o maior valor encontrado até o momento. 
    Dessa forma, evita comparações redundantes entre os elementos

    Args:
        array (List[int]): Lista de números inteiros

    Returns:
        int: Maior número presente no array
    """
    
    maior = array[0]

    for valor in array[1:]:
        if valor > maior:
            maior = valor

    return maior


numeros = [3, 7, 2, 9, 4]
resultado = greatest_number(numeros)

print("Maior número:", resultado)
