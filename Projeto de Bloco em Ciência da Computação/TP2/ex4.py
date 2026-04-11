import time
import random
import tracemalloc
from typing import List, Tuple


def particionar(lista: List[int], inicio: int, fim: int, comparacoes: List[int]) -> int:
    """
    Particiona o subarray em torno de um pivô aleatório e retorna o índice final do pivô

    Args:
        lista (List[int]): Lista sendo processada in-place
        inicio (int): Índice inicial do subarray atual
        fim (int): Índice final do subarray atual
        comparacoes (List[int]): Lista de um elemento usada como contador mutável de comparações

    Returns:
        int: Índice da posição definitiva do pivô após o particionamento
    """

    indice_pivo_aleatorio = random.randint(inicio, fim)
    lista[indice_pivo_aleatorio], lista[fim] = lista[fim], lista[indice_pivo_aleatorio]

    pivo = lista[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        comparacoes[0] += 1

        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]

    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]

    return i + 1


def quickselect(lista: List[int], inicio: int, fim: int, k: int, comparacoes: List[int]) -> int:
    """
    Encontra o k-ésimo menor elemento do subarray lista[inicio..fim] utilizando o algoritmo QuickSelect

    Args:
        lista (List[int]): Lista de inteiros sendo processada in-place
        inicio (int): Índice inicial do subarray atual
        fim (int): Índice final do subarray atual
        k (int): Índice do elemento buscado na ordem global
        comparacoes (List[int]): Lista de um elemento usada como contador mutável de comparações

    Returns:
        int: O k-ésimo menor elemento do subarray
    """

    if inicio == fim:
        return lista[inicio]

    indice_pivo = particionar(lista, inicio, fim, comparacoes)

    if k == indice_pivo:
        return lista[indice_pivo]

    elif k < indice_pivo:
        return quickselect(lista, inicio, indice_pivo - 1, k, comparacoes)

    else:
        return quickselect(lista, indice_pivo + 1, fim, k, comparacoes)


def buscar_kesimo_menor(lista: List[int], k: int) -> Tuple[int, int]:
    """
    Prepara e executa o QuickSelect para encontrar o k-ésimo menor elemento

    Args:
        lista (List[int]): Lista de inteiros onde a busca será realizada
        k (int): Posição do elemento desejado na ordem crescente

    Returns:
        Tuple[int, int]:
            - Valor do k-ésimo menor elemento encontrado
            - Total de comparações realizadas durante a busca
    """

    copia = lista[:]
    comparacoes = [0]
    k_zero = k - 1

    resultado = quickselect(copia, 0, len(copia) - 1, k_zero, comparacoes)
    return resultado, comparacoes[0]


def medir_desempenho(lista: List[int], k: int) -> Tuple[float, float, int, int]:
    """
    Executa o QuickSelect e registra tempo, memória de pico, comparações e resultado

    Args:
        lista (List[int]): Lista de inteiros onde a busca será realizada
        k (int): Posição do elemento desejado na ordem crescente

    Returns:
        Tuple[float, float, int, int]:
            - Tempo de execução em segundos
            - Memória de pico alocada durante a busca em KB
            - Total de comparações realizadas
            - Valor do k-ésimo menor elemento encontrado
    """

    tracemalloc.start()
    inicio = time.perf_counter()

    resultado, comparacoes = buscar_kesimo_menor(lista, k)

    tempo_total = time.perf_counter() - inicio
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return tempo_total, memoria_pico / 1024, comparacoes, resultado


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
    ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 1),
    ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 5),
    ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 10),
    ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 3),
    ([42], 1),
]

for i, (caso, k) in enumerate(casos_basicos):
    resultado, comparacoes = buscar_kesimo_menor(caso, k)
    esperado = sorted(caso)[k - 1]
    status = "✅" if resultado == esperado else "❌"
    print(f"Caso {i + 1}: k={k}, resultado={resultado}, comparações={comparacoes}, esperado={esperado} {status}")


print("\n\n===== Teste 2 - Análise de desempenho por tamanho de entrada =====\n")

tamanhos = list(range(25, 1001, 25))

print(f"{'Tamanho (n)':>12}  {'k':>6}  {'Resultado':>10}  {'Tempo (s)':>12}  {'Memória (KB)':>14}  {'Comparações':>13}")
print("-" * 75)

resultados = []

for tamanho in tamanhos:
    lista = gerar_lista_aleatoria(tamanho)
    k = random.randint(1, tamanho)
    tempo, memoria, comparacoes, resultado = medir_desempenho(lista, k)

    resultados.append({
        "n": tamanho,
        "k": k,
        "resultado": resultado,
        "tempo_s": tempo,
        "memoria_kb": memoria,
        "comparacoes": comparacoes,
    })

    print(f"{tamanho:>12}  {k:>6}  {resultado:>10}  {tempo:>12.6f}  {memoria:>14.4f}  {comparacoes:>13}")


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
