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
        """
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
            List[Tuple[str, int]]: Lista de pares (vizinho, peso) ordenada lexicograficamente pelo nome do vizinho
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


def dfs_recursiva(grafo: GrafoPonderado, vertice: str, visitados: Dict[str, bool], predecessores: Dict[str, Optional[str]], ordem_visita: List[str], profundidade: int) -> None:
    """
    Percorre o grafo em profundidade a partir de um vértice, respeitando ordem lexicográfica dos vizinhos e registrando os predecessores para reconstrução dos caminhos percorridos

    Args:
        grafo (GrafoPonderado): Grafo a ser percorrido
        vertice (str): Vértice atual do percurso
        visitados (Dict[str, bool]): Mapa de controle de vértices já visitados
        predecessores (Dict[str, Optional[str]]): Mapa que armazena o vértice anterior utilizado para alcançar cada vértice
        ordem_visita (List[str]): Lista acumuladora da ordem de visita
        profundidade (int): Profundidade atual no percurso, usada para exibição
    """

    visitados[vertice] = True
    ordem_visita.append(vertice)

    print(f"{'  ' * profundidade}visitando: {vertice}")

    for vizinho, _ in grafo.vizinhos_ordenados(vertice):
        if not visitados.get(vizinho, False):
            predecessores[vizinho] = vertice
            dfs_recursiva(grafo, vizinho, visitados, predecessores, ordem_visita, profundidade + 1)


def dfs(grafo: GrafoPonderado, origem: str) -> Tuple[List[str], Dict[str, Optional[str]]]:
    """
    Executa DFS a partir de um vértice de origem e retorna a ordem de visita juntamente com o mapa de predecessores.

    Args:
        grafo (GrafoPonderado): Grafo a ser percorrido
        origem (str): Vértice inicial da exploração

    Returns:
        Tuple[List[str], Dict[str, Optional[str]]]: Sequência de vértices na ordem em que foram descobertos, mapa de predecessores utilizado para reconstrução dos caminhos percorridos
    """

    visitados: Dict[str, bool] = {}
    predecessores: Dict[str, Optional[str]] = {origem: None}
    ordem_visita: List[str] = []
    dfs_recursiva(grafo, origem, visitados, predecessores, ordem_visita, 0)

    return ordem_visita, predecessores


def bfs(grafo: GrafoPonderado, origem: str) -> Tuple[ List[str], Dict[str, int], Dict[str, Optional[str]]]:
    """
    Executa BFS a partir de um vértice de origem e retorna a ordem de visita dos vértices, a camada de cada vértice e o mapa de predecessores utilizado para reconstrução dos caminhos encontrados pela busca

    Args:
        grafo (GrafoPonderado): Grafo a ser percorrido
        origem (str): Vértice inicial da exploração

    Returns:
        Tuple[List[str], Dict[str, int], Dict[str, Optional[str]]]: Sequência de vértices na ordem de visita, mapa de vértices para suas respectivas camadas, mapa de predecessores dos caminhos encontrados
    """

    visitados: Dict[str, bool] = {origem: True}
    camadas: Dict[str, int] = {origem: 0}
    predecessores: Dict[str, Optional[str]] = {origem: None}
    ordem_visita: List[str] = []
    fila: deque = deque([origem])

    while fila:
        vertice = fila.popleft()
        ordem_visita.append(vertice)

        for vizinho, _ in grafo.vizinhos_ordenados(vertice):
            if vizinho not in visitados:
                visitados[vizinho] = True
                camadas[vizinho] = camadas[vertice] + 1
                predecessores[vizinho] = vertice
                fila.append(vizinho)

    return ordem_visita, camadas, predecessores


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

    if predecessores.get(destino) is None and destino != origem:
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
    Calcula o custo total acumulado de um caminho somando os pesos das arestas percorridas

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
ordem_dfs, pred_dfs = dfs(grafo, "Berco_A")
ordem_bfs, camadas_bfs, pred_bfs = bfs(grafo, "Berco_A")
distancias, predecessores = dijkstra(grafo, "Berco_A")


print("\n===== Teste 1 - Ordem de Visita DFS =====\n")
print(f"Ordem DFS: {ordem_dfs}\n")


print("\n===== Teste 2 - Ordem de Visita BFS por Camada =====\n")
camadas_agrupadas: Dict[int, List[str]] = {}

for vertice, camada in camadas_bfs.items():
    if camada not in camadas_agrupadas:
        camadas_agrupadas[camada] = []

    camadas_agrupadas[camada].append(vertice)

print(f"{'Camada':<8}  {'Vértices'}")
print(f"{'-' * 8}  {'-' * 40}")

for camada in sorted(camadas_agrupadas):
    print(f"{camada:<8}  {sorted(camadas_agrupadas[camada])}")

print(f"\nOrdem BFS: {ordem_bfs}")


print("\n\n===== Teste 3 - Distâncias Mínimas pelo Dijkstra =====\n")
print(f"{'Destino':<20}  {'Custo mínimo':<14}  {'Caminho ótimo'}")
print(f"{'-' * 20}  {'-' * 14}  {'-' * 45}")

for vertice in grafo.vertices():
    caminho = reconstruir_caminho(predecessores, "Berco_A", vertice)
    caminho_str = " -> ".join(caminho) if caminho else "sem caminho"
    print(f"{vertice:<20}  {distancias[vertice]:<14}  {caminho_str}")


print("\n\n===== Teste 4 - Comparação das Três Ordens de Visita =====\n")
print(f"{'Posição':<10}  {'DFS':<20}  {'BFS':<20}")
print(f"{'-' * 10}  {'-' * 20}  {'-' * 20}")

for i, (v_dfs, v_bfs) in enumerate(zip(ordem_dfs, ordem_bfs), 1):
    print(f"{i:<10}  {v_dfs:<20}  {v_bfs:<20}")


print("\n\n===== Teste 5 - Custo Real dos Caminhos Encontrados por DFS e BFS =====\n")
destinos = ["Patio_1", "Patio_2", "Patio_3", "Alfandega", "Centro_Logistico", "Berco_B"]

print(f"{'Destino':<20}  {'Etapas DFS':<12}  {'Custo DFS':<12}  {'Etapas BFS':<12}  {'Custo BFS':<12}  {'Custo Dijkstra'}")
print(f"{'-' * 20}  {'-' * 12}  {'-' * 12}  {'-' * 12}  {'-' * 12}  {'-' * 14}")

for destino in destinos:
    cam_dij = reconstruir_caminho(predecessores, "Berco_A", destino)
    cam_dfs = reconstruir_caminho(pred_dfs, "Berco_A", destino)
    cam_bfs = reconstruir_caminho(pred_bfs, "Berco_A", destino)
    custo_dfs = calcular_custo(grafo, cam_dfs) if cam_dfs and len(cam_dfs) > 1 else 0
    custo_bfs = calcular_custo(grafo, cam_bfs) if cam_bfs and len(cam_bfs) > 1 else 0
    etapas_dfs = len(cam_dfs) - 1 if cam_dfs else 0
    etapas_bfs = len(cam_bfs) - 1 if cam_bfs else 0
    print(f"{destino:<20}  {etapas_dfs:<12}  {custo_dfs:<12}  {etapas_bfs:<12}  {custo_bfs:<12}  {distancias[destino]}")


print("\n\n===== Teste 6 - Vértices Visitados em Ordens Divergentes =====\n")
print(f"{'Vértice':<20}  {'Pos DFS':<10}  {'Pos BFS':<10}  {'Camada BFS':<12}  {'Custo Dijkstra'}")
print(f"{'-' * 20}  {'-' * 10}  {'-' * 10}  {'-' * 12}  {'-' * 14}")

for vertice in grafo.vertices():
    pos_dfs = ordem_dfs.index(vertice) + 1 if vertice in ordem_dfs else -1
    pos_bfs = ordem_bfs.index(vertice) + 1 if vertice in ordem_bfs else -1
    camada = camadas_bfs.get(vertice, -1)
    print(f"{vertice:<20}  {pos_dfs:<10}  {pos_bfs:<10}  {camada:<12}  {distancias[vertice]}")
print()
