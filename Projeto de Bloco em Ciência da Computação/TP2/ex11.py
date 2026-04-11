import random


N_ESTACOES = 20


def gerar_custos(n: int, seed: int = 42) -> tuple:
    """
    Gera aleatoriamente todos os custos do problema da linha de montagem

    Args:
        n (int): Número de estações em cada linha
        seed (int): Semente para reprodutibilidade

    Returns:
        tuple: Matrizes e vetores de custo (a, e, t, x)
    """

    random.seed(seed)

    a = [[random.randint(1, 20) for _ in range(n)] for _ in range(2)]
    e = [random.randint(1, 10) for _ in range(2)]
    t = [[random.randint(1, 10) for _ in range(n)] for _ in range(2)]
    x = [random.randint(1, 10) for _ in range(2)]

    return a, e, t, x


def tempo_minimo(i: int, j: int, a: list, e: list, t: list) -> int:
    """
    Calcula recursivamente o tempo mínimo para chegar à estação j da linha i

    Args:
        i (int): Índice da linha (0 ou 1)
        j (int): Índice da estação (0 a n-1)
        a (list): Tempos de montagem em cada estação
        e (list): Tempos de entrada em cada linha
        t (list): Tempos de transferência entre linhas

    Returns:
        int: Tempo mínimo acumulado até a estação j da linha i
    """

    if j == 0:
        return e[i] + a[i][0]

    custo_mesma_linha = tempo_minimo(i, j - 1, a, e, t) + a[i][j]
    custo_outra_linha = tempo_minimo(1 - i, j - 1, a, e, t) + t[1 - i][j - 1] + a[i][j]

    return min(custo_mesma_linha, custo_outra_linha)


def resolver_linha_montagem(n: int, a: list, e: list, t: list, x: list) -> tuple:
    """
    Resolve o problema da linha de montagem pela abordagem recursiva

    Args:
        n (int): Número de estações em cada linha
        a (list): Tempos de montagem em cada estação
        e (list): Tempos de entrada em cada linha
        t (list): Tempos de transferência entre linhas
        x (list): Tempos de saída de cada linha

    Returns:
        tuple: Tempo total mínimo e índice da linha de saída (0 ou 1)
    """

    tempo_linha_0 = tempo_minimo(0, n - 1, a, e, t) + x[0]
    tempo_linha_1 = tempo_minimo(1, n - 1, a, e, t) + x[1]

    if tempo_linha_0 <= tempo_linha_1:
        return tempo_linha_0, 0

    return tempo_linha_1, 1


def reconstruir_caminho(n: int, a: list, e: list, t: list) -> list:
    """
    Reconstrói o caminho ótimo rastreando as decisões da recursão

    Args:
        n (int): Número de estações em cada linha
        a (list): Tempos de montagem em cada estação
        e (list): Tempos de entrada em cada linha
        t (list): Tempos de transferência entre linhas

    Returns:
        list: Lista com o índice da linha escolhida em cada estação (0 ou 1)
    """

    caminho = [None] * n

    for j in range(n - 1, -1, -1):
        melhor_linha = None
        melhor_tempo = float("inf")

        for i in range(2):
            tempo = tempo_minimo(i, j, a, e, t)

            if tempo < melhor_tempo:
                melhor_tempo = tempo
                melhor_linha = i

        caminho[j] = melhor_linha

    return caminho


def exibir_instancia(n: int, a: list, e: list, t: list, x: list) -> None:
    """
    Exibe os parâmetros gerados para a instância do problema

    Args:
        n (int): Número de estações
        a (list): Tempos de montagem
        e (list): Tempos de entrada
        t (list): Tempos de transferência
        x (list): Tempos de saída
    """

    print(f"Número de estações por linha: {n}")
    print(f"Tempos de entrada e: {e}")
    print(f"Tempos de saída x: {x}")
    print()

    for i in range(2):
        print(f"Linha {i + 1} - tempos de montagem a[{i + 1}]: {a[i]}")

    print()

    for i in range(2):
        print(f"Linha {i + 1} - tempos de transferência t[{i + 1}]: {t[i]}")


def exibir_resultado(tempo_total: int, linha_saida: int, caminho: list) -> None:
    """
    Exibe o resultado da solução encontrada

    Args:
        tempo_total (int): Tempo mínimo total calculado
        linha_saida (int): Índice da linha por onde o chassi sai (0 ou 1)
        caminho (list): Sequência de linhas escolhidas em cada estação
    """

    print(f"Tempo mínimo total: {tempo_total}")
    print(f"Linha de saída: {linha_saida + 1}")
    print()

    sequencia = " -> ".join(f"L{linha + 1}" for linha in caminho)
    print(f"Caminho ótimo por estação: {sequencia}")


a, e, t, x = gerar_custos(N_ESTACOES)


print("\n===== Teste 1 - Instância do Problema =====\n")
exibir_instancia(N_ESTACOES, a, e, t, x)


print("\n\n===== Teste 2 - Solução Recursiva =====\n")
tempo_total, linha_saida = resolver_linha_montagem(N_ESTACOES, a, e, t, x)
caminho = reconstruir_caminho(N_ESTACOES, a, e, t)
exibir_resultado(tempo_total, linha_saida, caminho)


print("\n\n===== Teste 3 - Verificação por Estação =====\n")
for j in range(N_ESTACOES):
    f0 = tempo_minimo(0, j, a, e, t)
    f1 = tempo_minimo(1, j, a, e, t)
    print(f"Estação {j + 1:>2}  |  f(1,{j + 1}) = {f0:>4}   |   f(2,{j + 1}) = {f1:>4}")
