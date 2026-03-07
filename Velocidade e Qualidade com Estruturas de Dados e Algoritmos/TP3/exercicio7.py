from typing import List
contador_chamadas = 0


def knapsack_analisado(target: int, weights: List[int], index: int = 0) -> None:
    """
    Versão instrumentada do algoritmo knapsack para observar o crescimento do número de chamadas recursivas

    Args:
        target (int): Valor alvo da soma
        weights (List[int]): Lista de pesos disponíveis
        index (int): Índice atual da análise
    """

    global contador_chamadas
    contador_chamadas += 1

    if target == 0:
        return

    if target < 0 or index >= len(weights):
        return

    knapsack_analisado(target - weights[index], weights, index + 1)
    knapsack_analisado(target, weights, index + 1)


testes = [
    (10, [2, 3, 5]),
    (10, [2, 3, 5, 7]),
    (10, [1, 2, 3, 4, 5])
]
print("\n" + "=" * 40 + "\n")

for i, (alvo, pesos) in enumerate(testes):
    contador_chamadas = 0

    print(f"Teste {i+1}")
    print(f"Alvo: {alvo}")
    print(f"Pesos: {pesos}")

    knapsack_analisado(alvo, pesos)

    print("Total de chamadas recursivas:", contador_chamadas)
    print("Quantidade de pesos:", len(pesos))
    print("\n" + "=" * 40 + "\n")
