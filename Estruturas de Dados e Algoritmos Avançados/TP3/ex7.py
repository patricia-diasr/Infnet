from typing import List, Dict, Optional
from collections import deque


class GrafoDirecionado:
    """
    Grafo direcionado representado por lista de adjacência

    Attributes:
        _adjacencia (Dict[str, List[str]]): Mapa de cada vértice para seus sucessores diretos
    """

    def __init__(self) -> None:
        self._adjacencia: Dict[str, List[str]] = {}


    def adicionar_vertice(self, vertice: str) -> None:
        """
        Adiciona um vértice ao grafo caso ainda não exista

        Args:
            vertice (str): Nome do vértice a ser adicionado
        """

        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = []


    def adicionar_aresta(self, origem: str, destino: str) -> None:
        """
        Adiciona uma aresta direcionada de origem para destino

        Args:
            origem (str): Vértice de partida da aresta
            destino (str): Vértice de chegada da aresta
        """

        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self._adjacencia[origem].append(destino)


    def sucessores(self, vertice: str) -> List[str]:
        """
        Retorna os vértices alcançáveis diretamente a partir de um vértice

        Args:
            vertice (str): Vértice consultado

        Returns:
            List[str]: Lista de vértices sucessores
        """

        return self._adjacencia[vertice]


    def sucessores_ordenados(self, vertice: str) -> List[str]:
        """
        Retorna os vértices alcançáveis diretamente a partir de um vértice em ordem lexicográfica

        Args:
            vertice (str): Vértice consultado

        Returns:
            List[str]: Lista de vértices sucessores ordenada lexicograficamente
        """

        return sorted(self._adjacencia[vertice])


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

        return sum(len(v) for v in self._adjacencia.values())


    def __repr__(self) -> str:
        return f"GrafoDirecionado(vertices = {self.num_vertices()}, arestas = {self.num_arestas()})"


def _dfs_recursiva(grafo: GrafoDirecionado, vertice: str, visitados: Dict[str, bool], ordem_visita: List[str], profundidade: int) -> None:
    """
    Percorre o grafo direcionado em profundidade a partir de um vértice, respeitando ordem lexicográfica dos sucessores

    Args:
        grafo (GrafoDirecionado): Grafo a ser percorrido
        vertice (str): Vértice atual do percurso
        visitados (Dict[str, bool]): Mapa de controle de vértices já visitados
        ordem_visita (List[str]): Lista acumuladora da ordem de visita
        profundidade (int): Profundidade atual no percurso, usada para exibição
    """

    visitados[vertice] = True
    ordem_visita.append(vertice)

    print(f"{'  ' * profundidade}visitando: {vertice}")

    for sucessor in grafo.sucessores_ordenados(vertice):
        if not visitados.get(sucessor, False):
            _dfs_recursiva(grafo, sucessor, visitados, ordem_visita, profundidade + 1)


def dfs(grafo: GrafoDirecionado, origem: str) -> List[str]:
    """
    Executa DFS a partir de um vértice de origem e retorna a ordem de visita

    Args:
        grafo (GrafoDirecionado): Grafo a ser percorrido
        origem (str): Vértice inicial da exploração

    Returns:
        List[str]: Sequência de vértices na ordem em que foram descobertos
    """

    visitados: Dict[str, bool] = {}
    ordem_visita: List[str] = []
    _dfs_recursiva(grafo, origem, visitados, ordem_visita, 0)

    return ordem_visita


def bfs(grafo: GrafoDirecionado, origem: str) -> List[str]:
    """
    Executa BFS a partir de um vértice de origem e retorna a ordem de visita com a camada de cada vértice

    Args:
        grafo (GrafoDirecionado): Grafo a ser percorrido
        origem (str): Vértice inicial da exploração

    Returns:
        List[str]: Sequência de vértices na ordem em que foram descobertos
    """

    visitados: Dict[str, bool] = {origem: True}
    camadas: Dict[str, int] = {origem: 0}
    ordem_visita: List[str] = []
    fila: deque = deque([origem])

    while fila:
        vertice = fila.popleft()
        ordem_visita.append(vertice)

        for sucessor in grafo.sucessores_ordenados(vertice):
            if sucessor not in visitados:
                visitados[sucessor] = True
                camadas[sucessor] = camadas[vertice] + 1
                fila.append(sucessor)

    return ordem_visita, camadas


def construir_grafo_dependencias() -> GrafoDirecionado:
    """
    Constrói o grafo de dependências de tarefas definido no enunciado

    Returns:
        GrafoDirecionado: Grafo preenchido com todas as dependências
    """

    grafo = GrafoDirecionado()
    arestas = [
        ("Inicio", "A"),
        ("Inicio", "B"),
        ("A", "C"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
        ("B", "F"),
        ("F", "E"),
    ]

    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)

    return grafo


print("\n===== Teste 1 - DFS a Partir de Início =====\n")
grafo = construir_grafo_dependencias()
print(f"Grafo construído: {grafo}\n")
print("Percurso DFS (recuos indicam profundidade):\n")
ordem_dfs = dfs(grafo, "Inicio")
print(f"\nOrdem DFS: {ordem_dfs}")


print("\n\n===== Teste 2 - BFS a Partir de Início =====\n")
ordem_bfs, camadas = bfs(grafo, "Inicio")
print(f"{'Posição':<10}  {'Vértice':<10}  {'Camada'}")
print(f"{'-' * 10}  {'-' * 10}  {'-' * 6}")

for i, vertice in enumerate(ordem_bfs, 1):
    print(f"{i:<10}  {vertice:<10}  {camadas[vertice]}")

print(f"\nOrdem BFS: {ordem_bfs}")


print("\n\n===== Teste 3 - Comparação DFS x BFS =====\n")
print(f"{'Posição':<10}  {'DFS':<10}  {'BFS':<10}  {'Mesma ordem'}")
print(f"{'-' * 10}  {'-' * 10}  {'-' * 10}  {'-' * 12}")

for i, (dfs_v, bfs_v) in enumerate(zip(ordem_dfs, ordem_bfs), 1):
    mesma = "sim" if dfs_v == bfs_v else "não"
    print(f"{i:<10}  {dfs_v:<10}  {bfs_v:<10}  {mesma}")

divergencias = sum(1 for d, b in zip(ordem_dfs, ordem_bfs) if d != b)
print(f"\nPosições com ordens diferentes: {divergencias} de {len(ordem_dfs)}")


print("\n\n===== Teste 4 - Influência da Direção das Arestas =====\n")
pares = [("A", "Inicio"), ("C", "B"), ("E", "D"), ("E", "F")]
print("Tentativa de percurso em sentido contrário às arestas:\n")
print(f"{'Tentativa':<15}  {'Vértices alcançados pela BFS'}")
print(f"{'-' * 15}  {'-' * 30}")

for origem, destino in pares:
    ordem_inv, _ = bfs(grafo, origem)
    alcancou = destino in ordem_inv
    print(f"{origem} -> {destino:<8}  alcançou '{destino}': {alcancou}  percurso: {ordem_inv}")


print("\n\n===== Teste 5 - Vértices por Camada na BFS =====\n")
camadas_agrupadas: Dict[int, List[str]] = {}

for vertice, camada in camadas.items():
    if camada not in camadas_agrupadas:
        camadas_agrupadas[camada] = []

    camadas_agrupadas[camada].append(vertice)

print(f"{'Camada':<8}  {'Vértices'}")
print(f"{'-' * 8}  {'-' * 30}")

for camada in sorted(camadas_agrupadas):
    print(f"{camada:<8}  {sorted(camadas_agrupadas[camada])}")


print("\n\n===== Teste 6 - Sucessores de Cada Vértice =====\n")
print(f"{'Vértice':<10}  {'Sucessores diretos'}")
print(f"{'-' * 10}  {'-' * 25}")

for vertice in grafo.vertices():
    print(f"{vertice:<10}  {grafo.sucessores_ordenados(vertice)}")
print()
