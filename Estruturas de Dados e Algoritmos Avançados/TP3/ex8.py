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
            List[Tuple[str, int]]: Lista de pares (vizinho, peso) em ordem de inserção
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


def bfs_alcancaveis(grafo: GrafoPonderado, origem: str) -> List[str]:
    """
    Identifica todas as áreas alcançáveis a partir de uma origem usando BFS, ignorando os pesos das arestas

    Args:
        grafo (GrafoPonderado): Grafo ponderado a ser percorrido
        origem (str): Vértice de partida

    Returns:
        List[str]: Lista de vértices alcançáveis na ordem em que foram descobertos
    """

    visitados: Dict[str, bool] = {origem: True}
    ordem_visita: List[str] = [origem]
    fila: deque = deque([origem])

    while fila:
        atual = fila.popleft()

        for vizinho, _ in grafo.vizinhos_ordenados(atual):
            if vizinho not in visitados:
                visitados[vizinho] = True
                ordem_visita.append(vizinho)
                fila.append(vizinho)

    return ordem_visita


def bfs_menor_caminho(grafo: GrafoPonderado, origem: str, destino: str) -> Tuple[Optional[List[str]], int, int]:
    """
    Encontra o caminho com menor número de etapas entre dois vértices usando BFS e calcula seu custo total

    Args:
        grafo (GrafoPonderado): Grafo ponderado a ser percorrido
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        Tuple[Optional[List[str]], int, int]: Tripla com o caminho reconstruído, o número de etapas e o custo total acumulado, ou None, -1 e -1 se não houver caminho
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
                    caminho = _reconstruir_caminho(predecessores, origem, destino)
                    custo = _calcular_custo(grafo, caminho)
                    return caminho, len(caminho) - 1, custo

    return None, -1, -1


def _reconstruir_caminho(predecessores: Dict[str, Optional[str]], origem: str, destino: str) -> List[str]:
    """
    Reconstrói o caminho a partir do mapa de predecessores gerado pela BFS

    Args:
        predecessores (Dict[str, Optional[str]]): Mapa de cada vértice para o vértice que o descobriu
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        List[str]: Lista de vértices que formam o caminho de origem até destino
    """

    caminho: List[str] = []
    atual: Optional[str] = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()
    return caminho


def _calcular_custo(grafo: GrafoPonderado, caminho: List[str]) -> int:
    """
    Calcula o custo total acumulado de um caminho somando os pesos das arestas percorridas

    Args:
        grafo (GrafoPonderado): Grafo ponderado com os custos das arestas
        caminho (List[str]): Sequência de vértices do caminho

    Returns:
        int: Soma dos pesos das arestas ao longo do caminho
    """

    custo_total = 0

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]

        for vizinho, peso in grafo.vizinhos(origem):
            if vizinho == destino:
                custo_total += peso
                break

    return custo_total


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


print("\n===== Teste 1 - Áreas Alcançáveis a Partir de Cada Berço =====\n")
grafo = construir_rede_logistica()
print(f"Rede construída: {grafo}\n")

for origem in ["Berco_A", "Berco_B"]:
    alcancaveis = bfs_alcancaveis(grafo, origem)
    print(f"Origem: {origem}")
    print(f"Áreas alcançáveis ({len(alcancaveis)}): {alcancaveis}\n")


print("\n===== Teste 2 - Menor Caminho em Etapas entre Berco_A e Centro_Logistico =====\n")
caminho, etapas, custo = bfs_menor_caminho(grafo, "Berco_A", "Centro_Logistico")
print(f"Caminho: {' -> '.join(caminho)}")
print(f"Número de etapas: {etapas}")
print(f"Custo total desse caminho: {custo}")


print("\n\n===== Teste 3 - Todos os Caminhos com Dois Saltos a Partir de Berco_A =====\n")
destinos = ["Patio_1", "Patio_2", "Patio_3", "Alfandega", "Centro_Logistico", "Berco_B"]
print(f"{'Destino':<20}  {'Etapas':<8}  {'Custo':<8}  {'Caminho'}")
print(f"{'-' * 20}  {'-' * 8}  {'-' * 8}  {'-' * 45}")

for destino in destinos:
    cam, etap, cust = bfs_menor_caminho(grafo, "Berco_A", destino)
    caminho_str = " -> ".join(cam) if cam else "sem caminho"
    print(f"{destino:<20}  {etap:<8}  {cust:<8}  {caminho_str}")


print("\n\n===== Teste 4 - Custo de Caminhos Alternativos com Mesma Quantidade de Etapas =====\n")
caminhos_alternativos = [
    ["Berco_A", "Patio_1", "Alfandega", "Centro_Logistico"],
    ["Berco_A", "Patio_2", "Alfandega", "Centro_Logistico"],
    ["Berco_A", "Patio_2", "Patio_3", "Centro_Logistico"]
]
print(f"{'Caminho':<55}  {'Etapas':<8}  {'Custo'}")
print(f"{'-' * 55}  {'-' * 8}  {'-' * 6}")

for cam in caminhos_alternativos:
    custo_alt = _calcular_custo(grafo, cam)
    destaque = " <- menor custo" if custo_alt == min(_calcular_custo(grafo, c) for c in caminhos_alternativos) else ""
    print(f"{' -> '.join(cam):<55}  {len(cam) - 1:<8}  {custo_alt}{destaque}")


print("\n\n===== Teste 5 - Lista de Adjacência com Pesos =====\n")
print(f"{'Vértice':<20}  {'Conexões (vizinho, custo)'}")
print(f"{'-' * 20}  {'-' * 45}")

for vertice in grafo.vertices():
    print(f"{vertice:<20}  {grafo.vizinhos_ordenados(vertice)}")
print()