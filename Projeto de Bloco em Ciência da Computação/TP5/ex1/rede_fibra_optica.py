from typing import List, Optional, Tuple


NUM_CIDADES = 30

CONEXOES = [
    (0, 1, 45, 3), (0, 2, 60, 8), (0, 3, 75, 12), (1, 2, 20, 2), (1, 4, 55, 6),
    (2, 3, 35, 4), (2, 5, 40, 5), (3, 6, 80, 10), (4, 5, 15, 1), (4, 7, 90, 14),
    (5, 6, 30, 3), (5, 8, 50, 7), (6, 9, 65, 9), (7, 8, 25, 2), (7, 10, 70, 11),
    (8, 9, 45, 5), (8, 11, 60, 8), (9, 12, 85, 13), (10, 11, 15, 1), (10, 13, 50, 6),
    (11, 12, 40, 4), (11, 14, 55, 7), (12, 15, 75, 10), (13, 14, 30, 3), (13, 16, 65, 9),
    (14, 15, 35, 4), (14, 17, 45, 6), (15, 18, 90, 15), (16, 17, 20, 2), (16, 19, 55, 8),
    (17, 18, 40, 5), (17, 20, 60, 9), (18, 21, 80, 12), (19, 20, 25, 3), (19, 22, 70, 11),
    (20, 21, 35, 4), (20, 23, 50, 7), (21, 24, 75, 10), (22, 23, 15, 1), (22, 25, 60, 8),
    (23, 24, 45, 6), (23, 26, 55, 7), (24, 27, 90, 14), (25, 26, 30, 3), (25, 28, 65, 9),
    (26, 27, 40, 5), (26, 29, 70, 11), (27, 29, 50, 6), (28, 29, 25, 2), (0, 4, 110, 18),
    (1, 5, 85, 11), (2, 6, 95, 14), (3, 9, 120, 22), (4, 8, 70, 9), (5, 9, 60, 8),
    (6, 12, 110, 16), (7, 11, 65, 9), (8, 12, 80, 11), (9, 15, 130, 24), (10, 14, 55, 7),
    (11, 15, 70, 9), (12, 18, 115, 19), (13, 17, 60, 8), (14, 18, 75, 10), (15, 21, 140, 25),
    (16, 20, 65, 9), (17, 21, 85, 12), (18, 24, 125, 20), (19, 23, 60, 8), (20, 24, 80, 11),
    (21, 27, 135, 23), (22, 26, 55, 7), (23, 27, 75, 10), (24, 29, 110, 17), (0, 7, 200, 35),
    (3, 12, 180, 28), (10, 19, 150, 22), (13, 22, 140, 21), (16, 25, 160, 26), (1, 8, 95, 13),
    (2, 9, 105, 15), (7, 13, 85, 12), (11, 17, 90, 13), (19, 25, 80, 12), (20, 26, 85, 13)
]


class UnionFind:
    """
    Estrutura de conjuntos disjuntos com union por rank e path compression

    Attributes:
        pai (List[int]): Vetor onde pai[i] é o representante do conjunto de i
        rank (List[int]): Vetor de rank usado para manter a árvore achatada
    """

    def __init__(self, n: int) -> None:
        self.pai: List[int] = list(range(n))
        self.rank: List[int] = [0] * n


    def encontrar(self, x: int) -> int:
        """
        Retorna o representante do conjunto de x com path compression

        Args:
            x (int): Elemento a ser consultado

        Returns:
            int: Raiz do conjunto ao qual x pertence
        """

        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])

        return self.pai[x]


    def unir(self, x: int, y: int) -> bool:
        """
        Une os conjuntos de x e y usando union por rank

        Args:
            x (int): Primeiro elemento
            y (int): Segundo elemento

        Returns:
            bool: True se os elementos estavam em conjuntos distintos e foram unidos, False se já pertenciam ao mesmo conjunto
        """

        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)

        if raiz_x == raiz_y:
            return False

        if self.rank[raiz_x] < self.rank[raiz_y]:
            self.pai[raiz_x] = raiz_y

        elif self.rank[raiz_x] > self.rank[raiz_y]:
            self.pai[raiz_y] = raiz_x

        else:
            self.pai[raiz_y] = raiz_x
            self.rank[raiz_x] += 1

        return True


class HeapMinimo:
    """
    Heap mínimo implementado sobre uma lista de tuplas (prioridade, valor)

    Attributes:
        dados (List[Tuple[int, int]]): Lista interna que representa o heap
    """

    def __init__(self) -> None:
        self.dados: List[Tuple[int, int]] = []


    def _subir(self, i: int) -> None:
        """
        Restaura a propriedade de heap subindo o elemento na posição i

        Args:
            i (int): Índice do elemento a ser subido
        """

        while i > 0:
            pai = (i - 1) // 2

            if self.dados[pai][0] > self.dados[i][0]:
                self.dados[pai], self.dados[i] = self.dados[i], self.dados[pai]
                i = pai

            else:
                break


    def _descer(self, i: int) -> None:
        """
        Restaura a propriedade de heap descendo o elemento na posição i

        Args:
            i (int): Índice do elemento a ser descido
        """

        n = len(self.dados)

        while True:
            menor = i
            esq = 2 * i + 1
            dir = 2 * i + 2

            if esq < n and self.dados[esq][0] < self.dados[menor][0]:
                menor = esq

            if dir < n and self.dados[dir][0] < self.dados[menor][0]:
                menor = dir

            if menor != i:
                self.dados[i], self.dados[menor] = self.dados[menor], self.dados[i]
                i = menor

            else:
                break


    def inserir(self, prioridade: int, valor: int) -> None:
        """
        Insere um elemento no heap com a prioridade informada

        Args:
            prioridade (int): Valor usado para ordenação no heap
            valor (int): Dado associado ao elemento
        """

        self.dados.append((prioridade, valor))
        self._subir(len(self.dados) - 1)


    def extrair_minimo(self) -> Tuple[int, int]:
        """
        Remove e retorna o elemento de menor prioridade do heap

        Returns:
            Tuple[int, int]: Par (prioridade, valor) do elemento mínimo
        """

        self.dados[0], self.dados[-1] = self.dados[-1], self.dados[0]
        minimo = self.dados.pop()
        if self.dados:
            self._descer(0)

        return minimo


    def vazio(self) -> bool:
        """
        Verifica se o heap está vazio

        Returns:
            bool: True se não houver elementos, False caso contrário
        """

        return len(self.dados) == 0


def kruskal(num_cidades: int, conexoes: List[Tuple[int, int, int, int]]) -> Tuple[List[Tuple[int, int, int, int]], int]:
    """
    Encontra a árvore geradora mínima pelo custo usando o algoritmo de Kruskal

    Args:
        num_cidades (int): Número total de vértices no grafo
        conexoes (List[Tuple[int, int, int, int]]): Lista de arestas no formato (origem, destino, custo, latência)

    Returns:
        Tuple[List[Tuple[int, int, int, int]], int]: Par contendo a lista de arestas da AGM e o custo total
    """

    arestas_ordenadas = _ordenar_por_custo(conexoes)
    uf = UnionFind(num_cidades)
    agm: List[Tuple[int, int, int, int]] = []
    custo_total = 0

    for origem, destino, custo, latencia in arestas_ordenadas:
        if uf.unir(origem, destino):
            agm.append((origem, destino, custo, latencia))
            custo_total += custo

            if len(agm) == num_cidades - 1:
                break

    return agm, custo_total


def _ordenar_por_custo(conexoes: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
    """
    Ordena a lista de conexões pelo custo em ordem crescente usando insertion sort

    Args:
        conexoes (List[Tuple[int, int, int, int]]): Lista de arestas a ordenar

    Returns:
        List[Tuple[int, int, int, int]]: Nova lista ordenada por custo
    """

    lista = list(conexoes)

    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1

        while j >= 0 and lista[j][2] > chave[2]:
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = chave

    return lista


def dijkstra(num_cidades: int, conexoes: List[Tuple[int, int, int, int]], origem: int) -> Tuple[List[int], List[Optional[int]]]:
    """
    Calcula a menor latência acumulada da cidade de origem até todas as demais usando Dijkstra

    Args:
        num_cidades (int): Número total de vértices no grafo
        conexoes (List[Tuple[int, int, int, int]]): Lista de arestas no formato (origem, destino, custo, latência)
        origem (int): Cidade de partida para o cálculo das latências

    Returns:
        Tuple[List[int], List[Optional[int]]]: Vetor de distâncias mínimas e vetor de predecessores
    """

    grafo = _construir_lista_adjacencia(num_cidades, conexoes)
    INF = float("inf")

    distancias: List[float] = [INF] * num_cidades
    predecessores: List[Optional[int]] = [None] * num_cidades
    distancias[origem] = 0

    heap = HeapMinimo()
    heap.inserir(0, origem)

    while not heap.vazio():
        dist_atual, cidade_atual = heap.extrair_minimo()

        if dist_atual > distancias[cidade_atual]:
            continue

        for vizinho, latencia in grafo[cidade_atual]:
            nova_dist = distancias[cidade_atual] + latencia

            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                predecessores[vizinho] = cidade_atual
                heap.inserir(nova_dist, vizinho)

    return distancias, predecessores


def _construir_lista_adjacencia(num_cidades: int, conexoes: List[Tuple[int, int, int, int]]) -> List[List[Tuple[int, int]]]:
    """
    Constrói a lista de adjacência do grafo não-direcionado a partir das conexões

    Args:
        num_cidades (int): Número total de vértices
        conexoes (List[Tuple[int, int, int, int]]): Lista de arestas no formato (origem, destino, custo, latência)

    Returns:
        List[List[Tuple[int, int]]]: Lista de adjacência onde grafo[v] contém pares (vizinho, latência)
    """

    grafo: List[List[Tuple[int, int]]] = [[] for _ in range(num_cidades)]

    for origem, destino, _, latencia in conexoes:
        grafo[origem].append((destino, latencia))
        grafo[destino].append((origem, latencia))

    return grafo


print("\n===== Teste 1 - Etapa de Infraestrutura: Árvore Geradora Mínima (Kruskal) =====\n")

agm, custo_total = kruskal(NUM_CIDADES, CONEXOES)

print(f"{'#':>3}  {'Origem':>6}  {'Destino':>7}  {'Custo':>6}  {'Latência':>8}")
print(f"{'-'*3}  {'-'*6}  {'-'*7}  {'-'*6}  {'-'*8}")

for i, (origem, destino, custo, latencia) in enumerate(agm, 1):
    print(f"{i:>3}  {origem:>6}  {destino:>7}  {custo:>6}  {latencia:>8}")

print(f"\nTotal de conexões selecionadas: {len(agm)}")
print(f"Custo total da rede: {custo_total}")


print("\n\n===== Teste 2 - Etapa de Operação: Menor Latência a partir da Cidade 0 (Dijkstra) =====\n")

distancias, predecessores = dijkstra(NUM_CIDADES, CONEXOES, origem=0)

print(f"{'Cidade':>6}  {'Latência Acumulada (ms)':>23}  {'Predecessor':>11}")
print(f"{'-'*6}  {'-'*23}  {'-'*11}")

for cidade in range(1, NUM_CIDADES):
    lat = distancias[cidade]
    pred = predecessores[cidade]
    lat_str = str(lat) if lat != float("inf") else "inacessível"
    print(f"{cidade:>6}  {lat_str:>23}  {str(pred):>11}")


print("\n\n===== Teste 3 - Verificação de Conectividade =====\n")

inacessiveis = [c for c in range(1, NUM_CIDADES) if distancias[c] == float("inf")]

if inacessiveis:
    print(f"Cidades inacessíveis a partir da Cidade 0: {inacessiveis}")

else:
    print("Todas as cidades são alcançáveis a partir da Cidade 0")

print(f"\nMaior latência acumulada: {max(distancias[1:]):.0f} ms (Cidade {distancias.index(max(distancias[1:]))})")
print(f"Menor latência acumulada: {min(distancias[1:]):.0f} ms (Cidade {distancias.index(min(distancias[1:]))})\n")
