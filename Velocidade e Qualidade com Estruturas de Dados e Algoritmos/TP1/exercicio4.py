from typing import List

def busca_binaria(lista: List[int], alvo: int) -> int:
    """
    Realiza uma busca binária em uma lista ordenada

    A busca binária divide repetidamente o intervalo de busca ao meio, comparando o elemento 
    central com o valor desejado.

    Args:
        lista (List[int]): Lista de números onde a busca será realizada
        alvo (int): Valor que se deseja encontrar

    Returns:
        int: Índice do elemento encontrado. Retorna -1 caso o elemento não esteja na lista
    """
    
    inicio = 0
    fim = len(lista) - 1
    passos = 0

    while inicio <= fim:
        passos += 1
        meio = (inicio + fim) // 2

        if lista[meio] == alvo:
            print(f"Elemento encontrado em {passos} passo(s)")
            return meio
        elif lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1

    print(f"Elemento não encontrado após {passos} passo(s)")
    return -1


array = [2, 4, 6, 8, 10, 12, 13]
indice = busca_binaria(array, 8)

print("Índice retornado:", indice)
