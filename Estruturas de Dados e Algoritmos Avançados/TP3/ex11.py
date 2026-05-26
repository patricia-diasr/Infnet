import heapq
from typing import List, Dict, Optional, Tuple
from collections import deque


class GrafoPonderado:
    """
    Grafo não direcionado ponderado representado por lista de adjacência com pesos nas arestas

    Attributes:
        _adjacencia (Dict[str, List[Tuple[str, int]]]): Mapa de cada vértice para seus vizinhos e respectivos pesos
    """

    def __init__(self) -> None:
        self._adjacencia: Dict[str, List[Tuple[str, int]]] = {}


    def adicionar_vertice(self, vertice: str) -> None:
        """
        Adiciona um vértice ao grafo caso ainda não exista

        Args:
            vertice (str): Nome do vértice a ser adicionado
        """

        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = []


    def adicionar_aresta(self, a: str, b: str, peso: int) -> None:
        """9
        Adiciona uma aresta bidirecional ponderada entre dois vértices

        Args:
            a (str): Primeiro vértice da aresta
            b (str): Segundo vértice da aresta
            peso (int): Custo operacional do deslocamento entre os dois vértices
        """

        self.adicionar_vertice(a)
        self.adicionar_vertice(b)
        self._adjacencia[a].append((b, peso))
        self._adjacencia[b].append((a, peso))


    def vizinhos(self, vertice: str) -> List[Tuple[str, int]]:
        """
        Retorna os vizinhos de um vértice com seus respectivos pesos

        Args:
            vertice (str): Vértice consultado

        Returns:
            List[Tuple[str, int]]: Lista de pares (vizinho, peso)
        """

        return self._adjacencia[vertice]


    def vizinhos_ordenados(self, vertice: str) -> List[Tuple[str, int]]:
        """
        Retorna os vizinhos de um vértice com seus respectivos pesos em ordem lexicográfica

        Args:
            vertice (str): Vértice consultado

        Returns:
            List[Tuple[str, int]]: Lista de pares (vizinho, peso) ordenada lexicográficamente pelo nome do vizinho
        """

        return sorted(self._adjacencia[vertice], key=lambda par: par[0])


    def vertices(self) -> List[str]:
        """
        Retorna todos os vértices cadastrados no grafo

        Returns:
            List[str]: Lista de vértices
        """

        return list(self._adjacencia.keys())


    def num_vertices(self) -> int:
        """
        Retorna o número total de vértices no grafo

        Returns:
            int: Número de vértices
        """

        return len(self._adjacencia)


    def num_arestas(self) -> int:
        """
        Retorna o número total de arestas no grafo

        Returns:
            int: Número de arestas
        """

        return sum(len(v) for v in self._adjacencia.values()) // 2


    def __repr__(self) -> str:
        return f"GrafoPonderado(vertices = {self.num_vertices()}, arestas = {self.num_arestas()})"


def bfs_menor_caminho(grafo: GrafoPonderado, origem: str, destino: str) -> Tuple[Optional[List[str]], int, int]:
    """
    Encontra o caminho com menor némero de etapas entre dois vértices usando BFS e cálcula seu custo real

    Args:
        grafo (GrafoPonderado): Grafo ponderado a ser percorrido
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        Tuple[Optional[List[str]], int, int]: Tripla com o caminho reconstruído, o número de etapas e o custo real acumulado, ou None, -1 e -1 se não houver caminho
    """

    if origem == destino:
        return [origem], 0, 0

    predecessores: Dict[str, Optional[str]] = {origem: None}
    fila: deque = deque([origem])

    while fila:
        atual = fila.popleft()

        for vizinho, _ in grafo.vizinhos_ordenados(atual):
            if vizinho not in predecessores:
                predecessores[vizinho] = atual
                fila.append(vizinho)

                if vizinho == destino:
                    caminho = reconstruir_caminho(predecessores, origem, destino)
                    custo = calcular_custo(grafo, caminho)
                    return caminho, len(caminho) - 1, custo

    return None, -1, -1


def dijkstra(grafo: GrafoPonderado, origem: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
    """
    Executa o algoritmo de Dijkstra a partir de uma origem e calcula os menores custos até todos os vértices

    Args:
        grafo (GrafoPonderado): Grafo ponderado a ser percorrido
        origem (str): Vértice de partida

    Returns:
        Tuple[Dict[str, int], Dict[str, Optional[str]]]: Par com o mapa de distâncias mínimas de cada vértice e o mapa de predecessores que permite reconstruir os caminhos ótimos
    """

    distancias: Dict[str, int] = {v: float("inf") for v in grafo.vertices()}
    predecessores: Dict[str, Optional[str]] = {v: None for v in grafo.vertices()}
    distancias[origem] = 0
    heap: List[Tuple[int, str]] = [(0, origem)]

    while heap:
        custo_atual, vertice_atual = heapq.heappop(heap)

        if custo_atual > distancias[vertice_atual]:
            continue

        for vizinho, peso in grafo.vizinhos(vertice_atual):
            novo_custo = distancias[vertice_atual] + peso

            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                predecessores[vizinho] = vertice_atual
                heapq.heappush(heap, (novo_custo, vizinho))

    return distancias, predecessores


def reconstruir_caminho(predecessores: Dict[str, Optional[str]], origem: str, destino: str) -> Optional[List[str]]:
    """
    Reconstrói o caminho ótimo até um destino a partir do mapa de predecessores gerado pelo Dijkstra

    Args:
        predecessores (Dict[str, Optional[str]]): Mapa de cada vértice para o vértice que o relaxou
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        Optional[List[str]]: Lista de vértices que formam o caminho ótimo, ou None se não houver caminho
    """

    if predecessores[destino] is None and destino != origem:
        return None

    caminho: List[str] = []
    atual: Optional[str] = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()
    return caminho


def calcular_custo(grafo: GrafoPonderado, caminho: List[str]) -> int:
    """
    Cálcula o custo total acumulado de um caminho somando os pesos das arestas percorridas

    Args:
        grafo (GrafoPonderado): Grafo ponderado com os custos das arestas
        caminho (List[str]): Sequência de vértices do caminho

    Returns:
        int: Soma dos pesos das arestas ao longo do caminho
    """

    return sum(
        next(peso for v, peso in grafo.vizinhos(caminho[i]) if v == caminho[i + 1])
        for i in range(len(caminho) - 1)
    )


def construir_rede_logistica() -> GrafoPonderado:
    """
    Constrói a rede logística do porto com os custos operacionais definidos no enunciado

    Returns:
        GrafoPonderado: Grafo ponderado preenchido com todas as conexões e custos
    """

    grafo = GrafoPonderado()
    conexoes = [
        ("Berco_A", "Patio_1", 4),
        ("Berco_A", "Patio_2", 7),
        ("Berco_B", "Patio_2", 3),
        ("Berco_B", "Patio_3", 6),
        ("Patio_1", "Patio_2", 2),
        ("Patio_2", "Patio_3", 2),
        ("Patio_1", "Alfandega", 8),
        ("Patio_2", "Alfandega", 5),
        ("Patio_3", "Centro_Logistico", 4),
        ("Alfandega", "Centro_Logistico", 3)
    ]

    for a, b, peso in conexoes:
        grafo.adicionar_aresta(a, b, peso)

    return grafo


grafo = construir_rede_logistica()
distancias, predecessores_dijkstra = dijkstra(grafo, "Berco_A")
caminho_dijkstra = reconstruir_caminho(predecessores_dijkstra, "Berco_A", "Centro_Logistico")
custo_dijkstra = distancias["Centro_Logistico"]
caminho_bfs, etapas_bfs, custo_bfs = bfs_menor_caminho(grafo, "Berco_A", "Centro_Logistico")


print("\n===== Teste 1 - Resultado Direto de Cada Algoritmo =====\n")
print(f"{'Algoritmo':<12}  {'Caminho':<60}  {'Etapas':<8}  {'Custo'}")
print(f"{'-' * 12}  {'-' * 60}  {'-' * 8}  {'-' * 6}")
print(f"{'BFS':<12}  {' -> '.join(caminho_bfs):<60}  {etapas_bfs:<8}  {custo_bfs}")
print(f"{'Dijkstra':<12}  {' -> '.join(caminho_dijkstra):<60}  {len(caminho_dijkstra) - 1:<8}  {custo_dijkstra}")


print("\n\n===== Teste 2 - Custo Aresta a Aresta de Cada Caminho =====\n")
for nome, caminho in [("BFS", caminho_bfs), ("Dijkstra", caminho_dijkstra)]:
    print(f"Caminho {nome}:")
    print(f"  {'Trecho':<35}  {'Custo do trecho':<18}  {'Custo acumulado'}")
    print(f"  {'-' * 35}  {'-' * 18}  {'-' * 15}")
    acumulado = 0

    for i in range(len(caminho) - 1):
        trecho_origem = caminho[i]
        trecho_destino = caminho[i + 1]
        custo_trecho = next(peso for v, peso in grafo.vizinhos(trecho_origem) if v == trecho_destino)
        acumulado += custo_trecho
        trecho_str = f"{trecho_origem} -> {trecho_destino}"
        print(f"  {trecho_str:<35}  {custo_trecho:<18}  {acumulado}")
    
    print()


print("\n===== Teste 3 - Vértices em Comum e Divergentes entre os Caminhos =====\n")
conjunto_bfs = set(caminho_bfs)
conjunto_dijkstra = set(caminho_dijkstra)
em_comum = conjunto_bfs & conjunto_dijkstra
so_bfs = conjunto_bfs - conjunto_dijkstra
so_dijkstra = conjunto_dijkstra - conjunto_bfs
print(f"Vértices em comum: {sorted(em_comum)}")
print(f"Apenas no caminho BFS: {sorted(so_bfs) if so_bfs else 'nenhum'}")
print(f"Apenas no caminho Dijkstra: {sorted(so_dijkstra) if so_dijkstra else 'nenhum'}")


print("\n\n===== Teste 4 - Impacto dos Pesos Para Todos os Destinos =====\n")
print(f"{'Destino':<20}  {'Etapas BFS':<12}  {'Custo BFS':<12}  {'Etapas Dijkstra':<18}  {'Custo Dijkstra':<16}  {'Diferença de custo'}")
print(f"{'-' * 20}  {'-' * 12}  {'-' * 12}  {'-' * 18}  {'-' * 16}  {'-' * 18}")

for destino in grafo.vertices():
    if destino == "Berco_A":
        continue

    cam_bfs, etap_bfs, cust_bfs = bfs_menor_caminho(grafo, "Berco_A", destino)
    cam_dij = reconstruir_caminho(predecessores_dijkstra, "Berco_A", destino)
    cust_dij = distancias[destino]
    etap_dij = len(cam_dij) - 1 if cam_dij else -1
    diferenca = cust_bfs - cust_dij
    destaque = " <-" if diferenca > 0 else ""
    print(f"{destino:<20}  {etap_bfs:<12}  {cust_bfs:<12}  {etap_dij:<18}  {cust_dij:<16}  {diferenca}{destaque}")


print("\n\n===== Teste 5 - Casos em que BFS e Dijkstra Coincidem =====\n")
print(f"{'Destino':<20}  {'Mesmo caminho':<15}  {'Caminho'}")
print(f"{'-' * 20}  {'-' * 15}  {'-' * 45}")

for destino in grafo.vertices():
    if destino == "Berco_A":
        continue

    cam_bfs, _, _ = bfs_menor_caminho(grafo, "Berco_A", destino)
    cam_dij = reconstruir_caminho(predecessores_dijkstra, "Berco_A", destino)
    coincide = "sim" if cam_bfs == cam_dij else "não"
    print(f"{destino:<20}  {coincide:<15}  {' -> '.join(cam_bfs) if cam_bfs else 'sem caminho'}")
print()
