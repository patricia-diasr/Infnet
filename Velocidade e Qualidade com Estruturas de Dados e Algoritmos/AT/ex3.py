from typing import List, Tuple
import random
import time


def deduplicate_slow(arr: List[int]) -> Tuple[List[int], int]:
    """
    Remove duplicatas de forma ingênua, verificando cada elemento contra todos os anteriores já inseridos no resultado

    Args:
        arr (List[int]): Lista de inteiros possivelmente com repetições

    Returns:
        Tuple[List[int], int]:
            - lista sem duplicatas, mantendo a ordem de primeiro aparecimento
            - número de comparações realizadas
    """

    resultado: List[int] = []
    comparacoes = 0

    for elemento in arr:
        ja_existe = False
    
        for existente in resultado:
            comparacoes += 1
    
            if existente == elemento:
                ja_existe = True
                break
    
        if not ja_existe:
            resultado.append(elemento)

    return resultado, comparacoes


def deduplicate_fast(arr: List[int]) -> Tuple[List[int], int]:
    """
    Remove duplicatas em tempo O(n) utilizando um conjunto hash para verificação de pertencimento em O(1) amortizado

    Args:
        arr (List[int]): Lista de inteiros possivelmente com repetições

    Returns:
        Tuple[List[int], int]:
            - lista sem duplicatas, mantendo a ordem de primeiro aparecimento
            - número de "comparações" realizadas (buscas no conjunto)
    """

    vistos = set()
    resultado: List[int] = []
    comparacoes = 0

    for elemento in arr:
        comparacoes += 1

        if elemento not in vistos:
            vistos.add(elemento)
            resultado.append(elemento)

    return resultado, comparacoes


def testar_equivalencia_deduplicacao() -> None:
    """
    Verifica que deduplicate_slow e deduplicate_fast produzem saídas idênticas em todos os casos de teste definidos

    Raises:
        AssertionError: Se qualquer caso produzir resultados divergentes
    """

    casos = [
        [],
        [1],
        [1, 1, 1],
        [1, 2, 3, 4],
        [4, 3, 2, 1, 2, 3, 4],
        [1, 2, 1, 3, 2, 4, 3, 5],
        [7, 7, 7, 1, 7, 2, 1],
    ]

    for i, caso in enumerate(casos):
        saida_slow, _ = deduplicate_slow(caso)
        saida_fast, _ = deduplicate_fast(caso)
    
        assert saida_slow == saida_fast, (
            f"Caso {i+1}: divergência detectada!\n"
            f"=> slow={saida_slow}\n"
            f"=> fast={saida_fast}"
        )
        print(f"Caso {i+1}: entrada={caso} , saída={saida_fast} ✅ Equivalentes")


def k_smallest_sort(arr: List[int], k: int) -> Tuple[List[int], int, int]:
    """
    Encontra os k menores elementos ordenando toda a lista e retornando os k primeiros

    Args:
        arr (List[int]): Lista de inteiros
        k (int): Quantidade de menores elementos a retornar

    Returns:
        Tuple[List[int], int, int]:
            - lista com os k menores elementos em ordem crescente
            - número de comparações realizadas
            - número de cópias realizadas

    """

    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    copias = 0

    for i in range(1, n):
        chave = lista[i]
        copias += 1
        j = i - 1

        while j >= 0:
            comparacoes += 1
        
            if lista[j] > chave:
                lista[j + 1] = lista[j]
                copias += 1
                j -= 1
        
            else:
                break
        
        lista[j + 1] = chave
        copias += 1

    return lista[:k], comparacoes, copias


def particionar(lista: List[int], inicio: int, fim: int, contadores: dict) -> int:
    """
    Particionamento in-place para o QuickSelect, usando o último elemento como pivô. Contabiliza comparações e cópias no dicionário fornecido

    Args:
        lista (List[int]): Lista sendo processada (modificada in-place)
        inicio (int): Índice inicial do subarray
        fim (int): Índice final do subarray (pivô)
        contadores (dict): Acumula 'comparacoes' e 'copias'

    Returns:
        int: Posição final do pivô após a partição
    """

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        contadores["comparacoes"] += 1
    
        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
            contadores["copias"] += 3

    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
    contadores["copias"] += 3
    
    return i + 1


def k_smallest_quickselect(arr: List[int], k: int) -> Tuple[List[int], int, int]:
    """
    Encontra os k menores elementos usando QuickSelect para posicionar o k-ésimo menor na posição correta, sem ordenar o array por completo

    Args:
        arr (List[int]): Lista de inteiros
        k (int): Quantidade de menores elementos a retornar

    Returns:
        Tuple[List[int], int, int]:
            - lista com os k menores elementos em ordem crescente
            - número de comparações realizadas
            - número de cópias realizadas
    """

    lista = arr.copy()
    contadores = {"comparacoes": 0, "copias": 0}
    inicio, fim, alvo = 0, len(lista) - 1, k - 1

    while inicio <= fim:
        posicao_pivo = particionar(lista, inicio, fim, contadores)

        if posicao_pivo == alvo:
            break

        elif alvo < posicao_pivo:
            fim = posicao_pivo - 1
        
        else:
            inicio = posicao_pivo + 1

    return sorted(lista[:k]), contadores["comparacoes"], contadores["copias"]


def comparar_k_smallest(tamanhos: List[int], valores_k: List[float]) -> List[dict]:
    """
    Executa k_smallest_sort e k_smallest_quickselect para combinações de tamanho e fração k, registrando comparações, cópias e tempo

    Args:
        tamanhos (List[int]): Tamanhos dos arrays de teste
        valores_k (List[float]): Frações de n a usar como k

    Returns:
        List[dict]: Resultados com métricas para cada combinação testada
    """

    resultados = []

    for n in tamanhos:
        arr = list(range(1, n + 1))
        random.shuffle(arr)
        arr_dedup, _ = deduplicate_fast(arr)

        for fracao_k in valores_k:
            k = max(1, int(len(arr_dedup) * fracao_k))

            inicio = time.perf_counter()
            saida_sort, comp_sort, cop_sort = k_smallest_sort(arr_dedup, k)
            tempo_sort = time.perf_counter() - inicio

            inicio = time.perf_counter()
            saida_qs, comp_qs, cop_qs = k_smallest_quickselect(arr_dedup, k)
            tempo_qs = time.perf_counter() - inicio

            assert saida_sort == saida_qs, (
                f"Divergência k_smallest: n={n}, k={k}\n"
                f"sort={saida_sort[:5]}...\n  qs={saida_qs[:5]}..."
            )

            resultados.append({
                "n": n, "k": k, "fracao_k": fracao_k,
                "sort_comp": comp_sort, "sort_cop": cop_sort, "sort_t": tempo_sort,
                "qs_comp": comp_qs,   "qs_cop": cop_qs,   "qs_t": tempo_qs,
            })

    return resultados


def gerar_array_com_duplicatas(n: int, fator_duplicatas: float = 0.5) -> List[int]:
    """
    Gera um array aleatório de tamanho n com duplicatas

    Args:
        n (int): Tamanho do array
        fator_duplicatas (float): Fração do range de valores em relação a n. Valores menores geram mais duplicatas

    Returns:
        List[int]: Array de tamanho n com elementos repetidos
    """

    pool = list(range(1, max(2, int(n * fator_duplicatas)) + 1))
    return [random.choice(pool) for _ in range(n)]


random.seed(42)


print("\n===== Teste 1 - Equivalência de saída, deduplicate_slow vs fast =====\n")
testar_equivalencia_deduplicacao()

print("\n\n===== Teste 2 - Comparações por escala, slow O(n²) vs fast O(n) =====\n")

escalas_dedup = [1000, 10000, 25000, 50000, 100000]

print(f"{'n':>8}  {'slow_comp':>12}  {'fast_comp':>12}  {'razão slow/fast':>16}")
print("-" * 54)

for n in escalas_dedup:
    arr = gerar_array_com_duplicatas(n)

    _, comp_slow = deduplicate_slow(arr)
    _, comp_fast = deduplicate_fast(arr)

    razao = comp_slow / comp_fast if comp_fast else float("inf")
    print(f"{n:>8}  {comp_slow:>12}  {comp_fast:>12}  {razao:>15.1f}x")

print("\n\n===== Teste 3 - Validação do k_smallest (sort vs QuickSelect) =====\n")

casos_k = [
    ([5, 3, 8, 1, 9, 2, 7, 4, 6], 3),
    ([10, 20, 30, 40, 50], 2),
    ([1], 1),
    ([4, 4, 4, 1, 2], 3),
]

for i, (arr, k) in enumerate(casos_k):
    saida_sort, c_sort, _ = k_smallest_sort(arr, k)
    saida_qs,   c_qs,   _ = k_smallest_quickselect(arr, k)
    ok = "✅ Equivalentes " if saida_sort == saida_qs else "❌ Divergência"
    print(f"Caso {i+1}: arr={arr}  k={k}\n=> sort={saida_sort} (comp={c_sort}),  qs={saida_qs}, (comp={c_qs}), {ok}\n")


print("\n===== Teste 4 - Desempenho, k_smallest sobre arrays deduplicados =====\n")

tamanhos_k = [1000, 10000, 25000, 50000, 100000]
fracoes_k  = [0.05, 0.25, 0.50]

resultados_k = comparar_k_smallest(tamanhos_k, fracoes_k)

print(f"{'n':>8}  {'k':>6}  {'k/n':>6}  {'sort_comp':>12}  {'qs_comp':>10}  {'razão':>8}  {'sort_t(s)':>10}  {'qs_t(s)':>10}")
print("  " + "-" * 84)

for r in resultados_k:
    razao = r["sort_comp"] / r["qs_comp"] if r["qs_comp"] else float("inf")
    print(f"{r['n']:>8}  {r['k']:>6}  {r['fracao_k']:>6.0%}  {r['sort_comp']:>12}  {r['qs_comp']:>10}  {razao:>8.2f}x  {r['sort_t']:>10.5f}  {r['qs_t']:>10.5f}")
