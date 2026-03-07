from typing import List


def knapsack(target: int, weights: List[int], index: int = 0, atual: List[int] = None) -> List[List[int]]:
    """
    Encontra combinações de pesos que somam exatamente o valor alvo utilizando recursão

    Args:
        target (int): Valor alvo a ser atingido
        weights (List[int]): Lista de pesos disponíveis
        index (int): Índice atual da busca
        atual (List[int]): Combinação construída até o momento

    Returns:
        List[List[int]]: Lista contendo todas as combinações válidas encontradas
    """

    if atual is None:
        atual = []

    if target == 0:
        print(f"Combinação válida encontrada: {atual}")
        return [atual.copy()]

    if target < 0 or index >= len(weights):
        return []

    resultados = []
    atual.append(weights[index])
    resultados += knapsack(target - weights[index], weights, index + 1, atual)
    atual.pop()
    resultados += knapsack(target, weights, index + 1, atual)

    return resultados


testes = [
    (10, [2, 3, 5, 7]),
    (8, [1, 4, 5, 3]),
    (6, [1, 2, 3, 4])
]
print("\n" + "=" * 40 + "\n")

for i, (alvo, pesos) in enumerate(testes):
    print(f"Teste {i+1}")
    print(f"Alvo: {alvo}")
    print(f"Pesos disponíveis: {pesos}")

    combinacoes = knapsack(alvo, pesos)

    print("\nTotal de combinações encontradas:", len(combinacoes))
    print("Lista final:", combinacoes)
    print("\n" + "=" * 40 + "\n")
