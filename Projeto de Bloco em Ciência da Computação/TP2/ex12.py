import random
from functools import lru_cache


N_ESTACOES = 20
N_LINHAS = 3


def gerar_custos(n: int, linhas: int, seed: int = 42) -> tuple:
    """
    Gera aleatoriamente todos os custos do problema da linha de montagem

    Args:
        n (int): Número de estações em cada linha
        linhas (int): Número de linhas de montagem
        seed (int): Semente para reprodutibilidade

    Returns:
        tuple: Matrizes e vetores de custo (a, e, t, x)
    """

    random.seed(seed)

    a = [[random.randint(1, 20) for _ in range(n)] for _ in range(linhas)]
    e = [random.randint(1, 10) for _ in range(linhas)]
    t = [[[random.randint(1, 10) for _ in range(n)] for _ in range(linhas)] for _ in range(linhas)]
    x = [random.randint(1, 10) for _ in range(linhas)]

    return a, e, t, x


def criar_funcao_recursiva(a: list, e: list, t: list) -> callable:
    """
    Constrói e retorna a função recursiva de tempo mínimo com memoização

    Args:
        a (list): Tempos de montagem em cada estação
        e (list): Tempos de entrada em cada linha
        t (list): Tempos de transferência entre linhas, t[origem][destino][estacao]

    Returns:
        callable: Função recursiva tempo_minimo(i, j) com cache interno
    """

    a_t = tuple(tuple(linha) for linha in a)
    e_t = tuple(e)
    t_t = tuple(tuple(tuple(dest) for dest in orig) for orig in t)

    @lru_cache(maxsize=None)
    def tempo_minimo(i: int, j: int) -> int:
        """
        Calcula recursivamente o tempo mínimo para chegar à estação j da linha i

        Args:
            i (int): Índice da linha (0, 1 ou 2)
            j (int): Índice da estação (0 a n-1)

        Returns:
            int: Tempo mínimo acumulado até a estação j da linha i
        """

        if j == 0:
            return e_t[i] + a_t[i][0]

        melhor = float("inf")

        for k in range(N_LINHAS):
            custo = tempo_minimo(k, j - 1)

            if k != i:
                custo += t_t[k][i][j - 1]

            if custo < melhor:
                melhor = custo

        return melhor + a_t[i][j]

    return tempo_minimo


def resolver_linha_montagem(n: int, a: list, e: list, t: list, x: list) -> tuple:
    """
    Resolve o problema da linha de montagem com três linhas pela abordagem recursiva

    Args:
        n (int): Número de estações em cada linha
        a (list): Tempos de montagem em cada estação
        e (list): Tempos de entrada em cada linha
        t (list): Tempos de transferência entre linhas
        x (list): Tempos de saída de cada linha

    Returns:
        tuple: Tempo total mínimo, índice da linha de saída e a função recursiva utilizada
    """

    tempo_minimo = criar_funcao_recursiva(a, e, t)
    melhor_tempo = float("inf")
    melhor_linha = -1

    for i in range(N_LINHAS):
        tempo = tempo_minimo(i, n - 1) + x[i]

        if tempo < melhor_tempo:
            melhor_tempo = tempo
            melhor_linha = i

    return melhor_tempo, melhor_linha, tempo_minimo


def reconstruir_caminho(n: int, tempo_minimo: callable) -> list:
    """
    Reconstrói o caminho ótimo rastreando as decisões da recursão

    Args:
        n (int): Número de estações em cada linha
        tempo_minimo (callable): Função recursiva com cache já populado

    Returns:
        list: Lista com o índice da linha escolhida em cada estação (0, 1 ou 2)
    """

    caminho = [None] * n

    for j in range(n):
        melhor_linha = None
        melhor_tempo = float("inf")

        for i in range(N_LINHAS):
            tempo = tempo_minimo(i, j)

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
    print(f"Número de linhas: {N_LINHAS}")
    print(f"Tempos de entrada e: {e}")
    print(f"Tempos de saída x: {x}")
    print()

    for i in range(N_LINHAS):
        print(f"Linha {i + 1} - tempos de montagem  a[{i + 1}]: {a[i]}")

    print()

    for origem in range(N_LINHAS):
        for destino in range(N_LINHAS):
            if origem != destino:
                print(f"Transferência L{origem + 1}->L{destino + 1}  t[{origem + 1}][{destino + 1}]: {t[origem][destino]}")


def exibir_resultado(tempo_total: int, linha_saida: int, caminho: list) -> None:
    """
    Exibe o resultado da solução encontrada

    Args:
        tempo_total (int): Tempo mínimo total calculado
        linha_saida (int): Índice da linha por onde o chassi sai (0, 1 ou 2)
        caminho (list): Sequência de linhas escolhidas em cada estação
    """

    print(f"Tempo mínimo total: {tempo_total}")
    print(f"Linha de saída: {linha_saida + 1}")
    print()

    sequencia = " -> ".join(f"L{linha + 1}" for linha in caminho)
    print(f"Caminho ótimo por estação: {sequencia}")


a, e, t, x = gerar_custos(N_ESTACOES, N_LINHAS)


print("\n===== Teste 1 - Instância do Problema =====\n")
exibir_instancia(N_ESTACOES, a, e, t, x)


print("\n\n===== Teste 2 - Solução Recursiva =====\n")
tempo_total, linha_saida, tempo_minimo = resolver_linha_montagem(N_ESTACOES, a, e, t, x)
caminho = reconstruir_caminho(N_ESTACOES, tempo_minimo)
exibir_resultado(tempo_total, linha_saida, caminho)


print("\n\n===== Teste 3 - Verificação por Estação =====\n")
for j in range(N_ESTACOES):
    tempos = [tempo_minimo(i, j) for i in range(N_LINHAS)]
    valores = "  |  ".join(f"f({i + 1},{j + 1}) = {tempos[i]:>4}" for i in range(N_LINHAS))
    print(f"Estação {j + 1:>2} | {valores}")
