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


grafo = construir_rede_logistica()
distancias, predecessores = dijkstra(grafo, "Berco_A")
caminho = reconstruir_caminho(predecessores, "Berco_A", "Centro_Logistico")


print("\n===== Teste 1 - Caminho Mínimo Reconstruído =====\n")
print(f"Caminho: {' -> '.join(caminho)}")
print(f"Custo total: {distancias['Centro_Logistico']}")


print("\n\n===== Teste 2 - Navegação Reversa dos Predecessores =====\n")
print("Reconstrução passo a passo a partir de Centro_Logistico:\n")
atual = "Centro_Logistico"
passo = 1
print(f"{'Passo':<7}  {'Vértice atual':<20}  {'Predecessor'}")
print(f"{'-' * 7}  {'-' * 20}  {'-' * 20}")

while atual is not None:
    predecessor = predecessores[atual]
    valor = predecessor if predecessor else "raiz (sem predecessor)"
    print(f"{passo:<7}  {atual:<20}  {valor}")
    atual = predecessor
    passo += 1

print(f"\nCaminho reconstruído após reversão: {' -> '.join(caminho)}")


print("\n\n===== Teste 3 - Custo Acumulado Aresta a Aresta =====\n")
print(f"{'Trecho':<35}  {'Custo do trecho':<18}  {'Custo acumulado'}")
print(f"{'-' * 35}  {'-' * 18}  {'-' * 15}")
custo_acumulado = 0

for i in range(len(caminho) - 1):
    origem_trecho = caminho[i]
    destino_trecho = caminho[i + 1]
    custo_trecho = next(peso for v, peso in grafo.vizinhos(origem_trecho) if v == destino_trecho)
    custo_acumulado += custo_trecho
    trecho_str = f"{origem_trecho} -> {destino_trecho}"
    print(f"{trecho_str:<35}  {custo_trecho:<18}  {custo_acumulado}")


print("\n\n===== Teste 4 - Verificação de Otimalidade do Caminho =====\n")
caminhos_candidatos = [
    ["Berco_A", "Patio_1", "Alfandega", "Centro_Logistico"],
    ["Berco_A", "Patio_2", "Alfandega", "Centro_Logistico"],
    ["Berco_A", "Patio_2", "Patio_3", "Centro_Logistico"],
    ["Berco_A", "Patio_1", "Patio_2", "Alfandega", "Centro_Logistico"],
    ["Berco_A", "Patio_1", "Patio_2", "Patio_3", "Centro_Logistico"]
]
custos_candidatos = []

for candidato in caminhos_candidatos:
    custo = sum(
        next(peso for v, peso in grafo.vizinhos(candidato[i]) if v == candidato[i + 1])
        for i in range(len(candidato) - 1)
    )
    custos_candidatos.append(custo)

print(f"{'Caminho':<65}  {'Custo':<8}  {'Ótimo'}")
print(f"{'-' * 65}  {'-' * 8}  {'-' * 6}")
custo_otimo = distancias["Centro_Logistico"]

for candidato, custo in zip(caminhos_candidatos, custos_candidatos):
    otimo = "sim" if custo == custo_otimo else "não"
    destaque = " <-" if custo == custo_otimo else ""
    print(f"{' -> '.join(candidato):<65}  {custo:<8}  {otimo}{destaque}")


print("\n\n===== Teste 5 - Predecessores de Todos os Vértices =====\n")
print(f"{'Vértice':<20}  {'Predecessor':<20}  {'Custo mínimo'}")
print(f"{'-' * 20}  {'-' * 20}  {'-' * 12}")

for vertice in grafo.vertices():
    predecessor = predecessores[vertice] if predecessores[vertice] else "raiz"
    print(f"{vertice:<20}  {predecessor:<20}  {distancias[vertice]}")
print()
