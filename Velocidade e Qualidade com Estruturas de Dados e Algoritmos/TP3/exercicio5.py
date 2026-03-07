from typing import List
import time


def teams(candidates: List[str], k: int, inicio: int = 0, atual: List[str] = None, resultados: List[str] = None) -> List[str]:
    """
    Gera todas as combinações possíveis de tamanho k a partir de uma lista de candidatos

    Args:
        candidates (List[str]): Lista de candidatos disponíveis
        k (int): Tamanho das combinações desejadas
        inicio (int): Índice a partir do qual a busca continuará
        atual (List[str]): Combinação parcial em construção
        resultados (List[str]): Lista onde as combinações finais são armazenadas

    Returns:
        List[str]: Lista contendo todas as combinações geradas
    """

    if atual is None:
        atual = []

    if resultados is None:
        resultados = []

    if len(atual) == k:
        combinacao = ", ".join(atual)
        print(f"Combinação encontrada: {combinacao}")
        resultados.append(combinacao)
        return resultados

    for i in range(inicio, len(candidates)):
        atual.append(candidates[i])
        teams(candidates, k, i + 1, atual, resultados)
        atual.pop()

    return resultados


testes = [
    (["Ana", "Bruno", "Carlos", "Daiane"], 2),
    (["Ana", "Bruno", "Carlos", "Daiane"], 3),
    (["João", "Maria", "Pedro"], 2),
    (["A", "B", "C", "D", "E"], 3)
]

print("\n" + "=" * 40 + "\n")
for i, (candidatos, k) in enumerate(testes):
    print(f"Teste {i+1}")
    print("Candidatos:", candidatos)
    print("Tamanho do time (k):", k)

    combinacoes = teams(candidatos, k)

    print("\nTotal de combinações geradas:", len(combinacoes))
    print("Lista final:", combinacoes)
    print("\n" + "=" * 40 + "\n")
