import random
from typing import List

def ordenar_espadas_por_insercao(cartas: List[int]) -> List[int]:
    """
    Ordena as cartas de espadas utilizando o algoritmo de ordenação por inserção, simulando o 
    processo físico de organizar cartas na mão sob restrições específicas

    O algoritmo respeita as seguintes regras:
    - Apenas uma carta pode ser manipulada por vez
    - A carta visível da pilha embaralhada é retirada e inserida na posição correta entre as 
    cartas já seguradas na mão
    - A mão principal mantém sempre as cartas ordenadas
    - O processo termina quando todas as cartas estão organizadas em uma única pilha

    Args:
        cartas (List[int]): Lista contendo as cartas de espadas embaralhadas, onde os valores 
        variam de 1 (Ás) a 13 (Rei)

    Returns:
        List[int]: Lista contendo as cartas de espadas ordenadas em ordem crescente
    """
    
    mao_ordenada = []

    while cartas:
        # Outra mão pega a carta visível do topo
        carta = cartas.pop(0)

        # Encontra a posição correta na mão ordenada
        posicao = len(mao_ordenada)
        for i, valor in enumerate(mao_ordenada):
            if valor >= carta:
                posicao = i
                break

        # Insere a carta na posição adequada
        mao_ordenada.insert(posicao, carta)

    return mao_ordenada


cartas_espadas = list(range(1, 14))
random.shuffle(cartas_espadas)

print("Cartas embaralhadas:", cartas_espadas)
cartas_ordenadas = ordenar_espadas_por_insercao(cartas_espadas)
print("Cartas ordenadas:", cartas_ordenadas)
