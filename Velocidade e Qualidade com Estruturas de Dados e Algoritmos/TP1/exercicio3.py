from typing import List

def busca_linear(lista: List[int], alvo: int) -> int:
    """
    Realiza uma busca linear em uma lista ordenada ou não

    Percorre a lista elemento por elemento, comparando cada valor, com o elemento desejado, 
    até encontrá-lo ou até o fim da lista

    Args:
        lista (List[int]): Lista de números onde a busca será realizada
        alvo (int): Valor que se deseja encontrar

    Returns:
        int: Índice do elemento encontrado. Retorna -1 caso o elemento não esteja na lista
    """
    
    passos = 0

    for i in range(len(lista)):
        passos += 1
        
        if lista[i] == alvo:
            print(f"Elemento encontrado em {passos} passos")
            return i

    print(f"Elemento não encontrado após {passos} passos")
    return -1


array = [2, 4, 6, 8, 10, 12, 13]
indice = busca_linear(array, 8)

print("Índice retornado:", indice)
