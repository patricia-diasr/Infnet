from typing import List, Tuple, Dict


chamadas_recursivas_pura = 0
chamadas_recursivas_memo = 0


def knapsack_recursivo(target: int, weights: List[int], index: int = 0) -> int:
    """
    Versão recursiva pura do knapsack usada para análise de chamadas

    Args:
        target (int): Valor alvo
        weights (List[int]): Lista de pesos
        index (int): Índice atual

    Returns:
        int: Quantidade de combinações válidas
    """

    global chamadas_recursivas_pura
    chamadas_recursivas_pura += 1

    if target == 0:
        return 1

    if target < 0 or index >= len(weights):
        return 0

    incluir = knapsack_recursivo(target - weights[index], weights, index + 1)
    ignorar = knapsack_recursivo(target, weights, index + 1)

    return incluir + ignorar


def knapsack_memo(target: int, weights: List[int], index: int = 0, memo: Dict[Tuple[int, int], int] = None) -> int:
    """
    Versão otimizada do knapsack utilizando memoização

    Args:
        target (int): Valor alvo
        weights (List[int]): Lista de pesos
        index (int): Índice atual
        memo (dict): Estrutura para armazenar resultados intermediários

    Returns:
        int: Quantidade de combinações válidas
    """

    global chamadas_recursivas_memo

    if memo is None:
        memo = {}

    chamadas_recursivas_memo += 1
    chave = (target, index)

    if chave in memo:
        return memo[chave]

    if target == 0:
        return 1

    if target < 0 or index >= len(weights):
        return 0

    incluir = knapsack_memo(target - weights[index], weights, index + 1, memo)
    ignorar = knapsack_memo(target, weights, index + 1, memo)

    memo[chave] = incluir + ignorar
    return memo[chave]


testes = [
    (10, [2, 3, 5, 7]),
    (12, [1, 3, 4, 6, 8]),
    (15, [1, 2, 3, 5, 7, 10])
]
print("\n" + "=" * 40 + "\n")

for i, (alvo, pesos) in enumerate(testes):
    chamadas_recursivas_pura = 0
    chamadas_recursivas_memo = 0

    print(f"Teste {i+1}")
    print(f"Alvo: {alvo}")
    print(f"Pesos: {pesos}")

    resultado_puro = knapsack_recursivo(alvo, pesos)
    resultado_memo = knapsack_memo(alvo, pesos)

    print("Combinações encontradas:", resultado_puro)

    print("\nVersão recursiva pura:")
    print("Chamadas recursivas:", chamadas_recursivas_pura)
    
    print("\nVersão com memoização:")
    print("Chamadas recursivas:", chamadas_recursivas_memo)

    reducao = chamadas_recursivas_pura - chamadas_recursivas_memo
    print("\nRedução de chamadas:", reducao)
    print("\n" + "=" * 40 + "\n")
