import time
import random
import tracemalloc
from typing import List, Tuple


def particionar(lista: List[int], inicio: int, fim: int, comparacoes: List[int]) -> int:
    """
    Particiona o subarray em torno do pivô e retorna o índice final do pivô

    Args:
        lista (List[int]): Lista sendo ordenada in-place
        inicio (int): Índice inicial do subarray atual
        fim (int): Índice final do subarray atual; elemento nesta posição é o pivô
        comparacoes (List[int]): Lista de um elemento usada como contador mutável de comparações

    Returns:
        int: Índice da posição definitiva do pivô após o particionamento
    """

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        comparacoes[0] += 1

        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]

    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
    return i + 1


def quicksort(lista: List[int], inicio: int, fim: int, comparacoes: List[int]) -> None:
    """
    Ordena o subarray lista[inicio..fim] in-place utilizando o algoritmo QuickSort

    Args:
        lista (List[int]): Lista de inteiros sendo ordenada in-place
        inicio (int): Índice inicial do subarray atual
        fim (int): Índice final do subarray atual
        comparacoes (List[int]): Lista de um elemento usada como contador mutável de comparações
    """

    if inicio < fim:
        indice_pivo = particionar(lista, inicio, fim, comparacoes)
        quicksort(lista, inicio, indice_pivo - 1, comparacoes)
        quicksort(lista, indice_pivo + 1, fim, comparacoes)


def ordenar(lista: List[int]) -> Tuple[List[int], int]:
    """
    Prepara e executa o QuickSort sobre uma cópia da lista fornecida

    Args:
        lista (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[List[int], int]:
            - Cópia da lista em ordem crescente
            - Total de comparações realizadas durante a ordenação
    """

    copia = lista[:]
    comparacoes = [0]
    quicksort(copia, 0, len(copia) - 1, comparacoes)

    return copia, comparacoes[0]


def medir_desempenho(lista: List[int]) -> Tuple[float, float, int]:
    """
    Executa o QuickSort sobre a lista fornecida e registra tempo, memória de pico e comparações

    Args:
        lista (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[float, float, int]:
            - Tempo de execução em segundos
            - Memória de pico alocada durante a ordenação em KB
            - Total de comparações realizadas
    """

    tracemalloc.start()
    inicio = time.perf_counter()

    _, comparacoes = ordenar(lista)

    tempo_total = time.perf_counter() - inicio
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return tempo_total, memoria_pico / 1024, comparacoes


def gerar_lista_aleatoria(tamanho: int) -> List[int]:
    """
    Gera uma lista de inteiros únicos embaralhados aleatoriamente

    Args:
        tamanho (int): Quantidade de elementos da lista

    Returns:
        List[int]: Lista com os inteiros de 1 até tamanho em ordem aleatória
    """

    lista = list(range(1, tamanho + 1))
    random.shuffle(lista)
    return lista


random.seed(42)


print("\n===== Teste 1 - Validação do algoritmo =====\n")

casos_basicos = [
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [42],
    [],
]

for i, caso in enumerate(casos_basicos):
    ordenado, comparacoes = ordenar(caso)
    print(f"Caso {i + 1}: entrada={caso}, saída={ordenado}, comparações={comparacoes}")


print("\n\n===== Teste 2 - Análise de desempenho por tamanho de entrada =====\n")

tamanhos = list(range(25, 1001, 25))

print(f"{'Tamanho (n)':>12}  {'Tempo (s)':>12}  {'Memória (KB)':>14}  {'Comparações':>13}")
print("-" * 57)

resultados = []

for tamanho in tamanhos:
    lista = gerar_lista_aleatoria(tamanho)
    tempo, memoria, comparacoes = medir_desempenho(lista)

    resultados.append({
        "n": tamanho,
        "tempo_s": tempo,
        "memoria_kb": memoria,
        "comparacoes": comparacoes,
    })

    print(f"{tamanho:>12}  {tempo:>12.6f}  {memoria:>14.4f}  {comparacoes:>13}")


print("\n\n===== Teste 3 - Resumo estatístico =====\n")

tempos = [r["tempo_s"] for r in resultados]
memorias = [r["memoria_kb"] for r in resultados]
comparacoes_lista = [r["comparacoes"] for r in resultados]

print(f"Entradas avaliadas: {len(resultados)}")
print(f"Tempo mínimo: {min(tempos):.6f} s (n={resultados[tempos.index(min(tempos))]['n']})")
print(f"Tempo máximo: {max(tempos):.6f} s (n={resultados[tempos.index(max(tempos))]['n']})")
print(f"Memória de pico: {max(memorias):.4f} KB (n={resultados[memorias.index(max(memorias))]['n']})")
print(f"Comparações mín.: {min(comparacoes_lista)} (n={resultados[comparacoes_lista.index(min(comparacoes_lista))]['n']})")
print(f"Comparações máx.: {max(comparacoes_lista)} (n={resultados[comparacoes_lista.index(max(comparacoes_lista))]['n']})")
