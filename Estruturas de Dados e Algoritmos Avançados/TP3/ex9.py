import heapq
from typing import List, Dict, Optional, Tuple


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


print("\n===== Teste 1 - Distâncias Mínimas a Partir de Berco_A =====\n")
grafo = construir_rede_logistica()
print(f"Rede construída: {grafo}\n")
distancias, predecessores = dijkstra(grafo, "Berco_A")
print(f"{'Destino':<20}  {'Custo mínimo':<14}  {'Caminho ótimo'}")
print(f"{'-' * 20}  {'-' * 14}  {'-' * 45}")

for vertice in grafo.vertices():
    caminho = reconstruir_caminho(predecessores, "Berco_A", vertice)
    caminho_str = " -> ".join(caminho) if caminho else "sem caminho"
    custo = distancias[vertice]
    print(f"{vertice:<20}  {custo:<14}  {caminho_str}")


print("\n\n===== Teste 2 - Comparação Dijkstra x BFS para Centro_Logistico =====\n")
caminho_bfs = ["Berco_A", "Patio_1", "Alfandega", "Centro_Logistico"]
custo_bfs = sum(
    peso
    for i in range(len(caminho_bfs) - 1)
    for vizinho, peso in grafo.vizinhos(caminho_bfs[i])
    if vizinho == caminho_bfs[i + 1]
)
caminho_dijkstra = reconstruir_caminho(predecessores, "Berco_A", "Centro_Logistico")
custo_dijkstra = distancias["Centro_Logistico"]

print(f"{'Algoritmo':<12}  {'Etapas':<8}  {'Custo':<8}  {'Caminho'}")
print(f"{'-' * 12}  {'-' * 8}  {'-' * 8}  {'-' * 50}")
print(f"{'BFS':<12}  {len(caminho_bfs) - 1:<8}  {custo_bfs:<8}  {' -> '.join(caminho_bfs)}")
print(f"{'Dijkstra':<12}  {len(caminho_dijkstra) - 1:<8}  {custo_dijkstra:<8}  {' -> '.join(caminho_dijkstra)}")
print(f"\nRedução de custo com Dijkstra: {custo_bfs - custo_dijkstra} unidades")


print("\n\n===== Teste 3 - Dijkstra a Partir de Cada Vértice =====\n")
origens = ["Berco_A", "Berco_B", "Alfandega", "Centro_Logistico"]

for origem in origens:
    dist, _ = dijkstra(grafo, origem)
    custo_centro = dist["Centro_Logistico"] if origem != "Centro_Logistico" else 0
    custo_berco_a = dist["Berco_A"] if origem != "Berco_A" else 0
    print(f"Origem: {origem:<20}  custo até Centro_Logistico: {custo_centro:<6}  custo até Berco_A: {custo_berco_a}")


print("\n\n===== Teste 4 - Estado do Heap Durante Relaxamento a Partir de Berco_A =====\n")
distancias_passo: Dict[str, int] = {v: float("inf") for v in grafo.vertices()}
predecessores_passo: Dict[str, Optional[str]] = {v: None for v in grafo.vertices()}
distancias_passo["Berco_A"] = 0
heap_passo: List[Tuple[int, str]] = [(0, "Berco_A")]
passo = 1
print(f"{'Passo':<7}  {'Vértice extraído':<20}  {'Custo':<8}  {'Relaxamentos realizados'}")
print(f"{'-' * 7}  {'-' * 20}  {'-' * 8}  {'-' * 40}")

while heap_passo:
    custo_atual, vertice_atual = heapq.heappop(heap_passo)

    if custo_atual > distancias_passo[vertice_atual]:
        continue

    relaxamentos = []

    for vizinho, peso in grafo.vizinhos(vertice_atual):
        novo_custo = distancias_passo[vertice_atual] + peso
    
        if novo_custo < distancias_passo[vizinho]:
            distancias_passo[vizinho] = novo_custo
            predecessores_passo[vizinho] = vertice_atual
            heapq.heappush(heap_passo, (novo_custo, vizinho))
            relaxamentos.append(f"{vizinho}={novo_custo}")

    relaxamentos_str = ", ".join(relaxamentos) if relaxamentos else "nenhum"
    print(f"{passo:<7}  {vertice_atual:<20}  {custo_atual:<8}  {relaxamentos_str}")
    passo += 1


print("\n\n===== Teste 5 - Mapa de Predecessores Final =====\n")
print(f"{'Vértice':<20}  {'Predecessor no caminho ótimo'}")
print(f"{'-' * 20}  {'-' * 28}")

for vertice, predecessor in predecessores.items():
    valor = predecessor if predecessor else "raiz (sem predecessor)"
    print(f"{vertice:<20}  {valor}")
print()
