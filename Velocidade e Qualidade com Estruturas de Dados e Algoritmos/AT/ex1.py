from typing import List, Tuple
import random
import time


def busca_linear(arr: List[int], alvo: int) -> Tuple[int, int]:
    """
    Realiza a busca linear em um array, varrendo elemento por elemento

    Args:
        arr (List[int]): Array de inteiros a ser percorrido
        alvo (int): Valor a ser encontrado

    Returns:
        Tuple[int, int]:
            - posição encontrada ou -1
            - número de comparações realizadas
    """

    comparacoes = 0

    for i, elemento in enumerate(arr):
        comparacoes += 1

        if elemento == alvo:
            return i, comparacoes

    return -1, comparacoes


def busca_binaria(arr: List[int], alvo: int) -> Tuple[int, int]:
    """
    Realiza a busca binária em um array previamente ordenado

    Args:
        arr (List[int]): Array de inteiros ordenado em ordem crescente
        alvo (int): Valor a ser encontrado

    Returns:
        Tuple[int, int]:
            - posição encontrada ou -1
            - número de comparações realizadas

    Raises:
        ValueError: Se a pré-condição de ordenação falhar na verificação rápida
    """

    if len(arr) > 1 and arr[0] > arr[-1]:
        raise ValueError(f"Pré-condição violada: o array não parece estar ordenado (primeiro={arr[0]}, último={arr[-1]}). Ordene o array antes de chamar busca_binaria()")

    comparacoes = 0
    inicio, fim = 0, len(arr) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1

        if arr[meio] == alvo:
            return meio, comparacoes

        elif arr[meio] < alvo:
            inicio = meio + 1

        else:
            fim = meio - 1

    return -1, comparacoes


def gerar_vetores(n: int) -> dict:
    """
    Gera três variações de vetores com n elementos inteiros

    Args:
        n (int): Tamanho dos vetores gerados.

    Returns:
        dict: Dicionário com as chaves 'ordenado', 'reverso' e 'aleatorio', cada uma mapeando para um List[int] de tamanho n
    """

    base = list(range(1, n + 1))
    aleatorio = base.copy()
    random.shuffle(aleatorio)

    return {
        "ordenado": base,
        "reverso": base[::-1],
        "aleatorio": aleatorio,
    }


def coletar_metricas(escalas: List[int], alvo_relativo: float = 0.75) -> List[dict]:
    """
    Executa busca linear e binária em múltiplas escalas e cenários, registrando contagens de comparações e tempo de execução

    Args:
        escalas (List[int]): Lista com os tamanhos n de cada rodada
        alvo_relativo (float): Fração de n usada como alvo da busca (padrão 0.75)

    Returns:
        List[dict]: Lista de resultados, um dicionário por combinação (escala × cenário × algoritmo)
    """

    resultados = []

    for n in escalas:
        vetores = gerar_vetores(n)
        alvo = int(n * alvo_relativo)

        for nome_cenario, vetor in vetores.items():
            inicio = time.perf_counter()
            posicao_linear, comp_linear = busca_linear(vetor, alvo)
            tempo_linear = time.perf_counter() - inicio

            resultados.append({
                "n":          n,
                "cenario":    nome_cenario,
                "algoritmo":  "linear",
                "comparacoes": comp_linear,
                "posicao":    posicao_linear,
                "tempo_s":    tempo_linear,
            })

            if nome_cenario == "ordenado":
                inicio = time.perf_counter()
                posicao_binaria, comp_binaria = busca_binaria(vetor, alvo)
                tempo_binaria = time.perf_counter() - inicio

                resultados.append({
                    "n":          n,
                    "cenario":    nome_cenario,
                    "algoritmo":  "binaria",
                    "comparacoes": comp_binaria,
                    "posicao":    posicao_binaria,
                    "tempo_s":    tempo_binaria,
                })

    return resultados


print("\n===== Teste 1 - Validação dos algoritmos =====\n")

casos_basicos = [
    ([1, 3, 5, 7, 9], 5),
    ([1, 3, 5, 7, 9], 6),
    ([1, 3, 5, 7, 9], 1),
    ([1, 3, 5, 7, 9], 9),
]

for i, (arr, alvo) in enumerate(casos_basicos):
    pos_lin, comp_lin = busca_linear(arr, alvo)
    pos_bin, comp_bin = busca_binaria(arr, alvo)

    print(f"Caso {i+1}: array={arr}, alvo={alvo}")
    print(f"Linear -> posição={pos_lin}, comparações={comp_lin}")
    print(f"Binária -> posição={pos_bin}, comparações={comp_bin}")
    print()


print("\n===== Teste 2 - Pré-condição da busca binária =====\n")

arr_desordenado = [5, 1, 3, 9, 2]
print(f"Array desordenado: {arr_desordenado}")

try:
    busca_binaria(arr_desordenado, 3)
except ValueError as erro:
    print(f"ValueError capturado: {erro}\n")


print("\n===== Teste 3 - Métricas por escala e cenário =====\n")

escalas = [100, 1000, 10000, 100000, 1000000]
resultados = coletar_metricas(escalas)

print(f"{'n':>10}  {'cenário':<12}  {'algoritmo':<8}  {'comparações':>14}  {'tempo (s)':>12}")
print("-" * 64)

for r in resultados:
    print(f"{r['n']:>10}  {r['cenario']:<12}  {r['algoritmo']:<8}  {r['comparacoes']:>14}  {r['tempo_s']:>12.6f}")
