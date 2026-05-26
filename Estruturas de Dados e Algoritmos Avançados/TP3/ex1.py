from typing import List, Dict, Optional


class GrafoNaoDirecionado:
    """
    Grafo não direcionado representado por lista de adjacência

    Attributes:
        _num_vertices (int): Número total de vértices no grafo
        _adjacencia (Dict[int, List[int]]): Mapa de cada vértice para seus vizinhos
    """

    def __init__(self, num_vertices: int) -> None:
        self._num_vertices: int = num_vertices
        self._adjacencia: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}


    def adicionar_aresta(self, u: int, v: int) -> None:
        """
        Adiciona uma aresta não direcionada entre dois vértices

        Args:
            u (int): Primeiro vértice da aresta
            v (int): Segundo vértice da aresta
        """

        self._adjacencia[u].append(v)
        self._adjacencia[v].append(u)


    def vizinhos(self, vertice: int) -> List[int]:
        """
        Retorna a lista de vizinhos de um vértice

        Args:
            vertice (int): Vértice consultado

        Returns:
            List[int]: Lista de vértices adjacentes
        """

        return self._adjacencia[vertice]


    def num_vertices(self) -> int:
        """
        Retorna o número total de vértices do grafo

        Returns:
            int: Número de vértices
        """

        return self._num_vertices


    def __repr__(self) -> str:
        return f"GrafoNaoDirecionado(vertices = {self._num_vertices}, arestas = {sum(len(v) for v in self._adjacencia.values()) // 2})"


def _dfs(grafo: GrafoNaoDirecionado, vertice: int, visitados: List[bool]) -> None:
    """
    Percorre em profundidade todos os vértices alcançáveis a partir de um vértice inicial

    Args:
        grafo (GrafoNaoDirecionado): Grafo a ser percorrido
        vertice (int): Vértice de partida do percurso
        visitados (List[bool]): Vetor de controle de vértices já visitados
    """

    visitados[vertice] = True

    for vizinho in grafo.vizinhos(vertice):
        if not visitados[vizinho]:
            _dfs(grafo, vizinho, visitados)


def contar_componentes_conectadas(grafo: GrafoNaoDirecionado) -> int:
    """
    Conta o número de componentes conectadas em um grafo não direcionado usando DFS

    Args:
        grafo (GrafoNaoDirecionado): Grafo a ser analisado

    Returns:
        int: Número de componentes conectadas encontradas
    """

    visitados: List[bool] = [False] * grafo.num_vertices()
    componentes: int = 0

    for vertice in range(grafo.num_vertices()):
        if not visitados[vertice]:
            _dfs(grafo, vertice, visitados)
            componentes += 1

    return componentes


def formar_times(n: int, amizades: List[tuple]) -> int:
    """
    Recebe o número de alunos e as amizades e retorna quantos times independentes são formados

    Args:
        n (int): Número de alunos
        amizades (List[tuple]): Lista de pares (i, j) representando amizades

    Returns:
        int: Número de times independentes formados
    """

    grafo = GrafoNaoDirecionado(n)

    for i, j in amizades:
        grafo.adicionar_aresta(i, j)

    return contar_componentes_conectadas(grafo)


print("\n===== Teste 1 - Caso Básico com Três Grupos =====\n")
n1 = 7
amizades1 = [(0, 1), (1, 2), (3, 4), (5, 6)]
resultado1 = formar_times(n1, amizades1)
print(f"Alunos: {n1}")
print(f"Amizades: {amizades1}")
print(f"Times formados: {resultado1}")
print(f"Esperado: 3 (grupo 0-1-2, grupo 3-4, grupo 5-6)")


print("\n\n===== Teste 2 - Todos no Mesmo Time =====\n")
n2 = 5
amizades2 = [(0, 1), (1, 2), (2, 3), (3, 4)]
resultado2 = formar_times(n2, amizades2)
print(f"Alunos: {n2}")
print(f"Amizades: {amizades2}")
print(f"Times formados: {resultado2}")
print(f"Esperado: 1 (todos conectados em cadeia)")


print("\n\n===== Teste 3 - Nenhuma Amizade =====\n")
n3 = 4
amizades3 = []
resultado3 = formar_times(n3, amizades3)
print(f"Alunos: {n3}")
print(f"Amizades: {amizades3}")
print(f"Times formados: {resultado3}")
print(f"Esperado: 4 (cada aluno forma seu próprio time)")


print("\n\n===== Teste 4 - Amizades Transitivas Formando Grupos =====\n")
n4 = 6
amizades4 = [(0, 1), (2, 3), (3, 5), (2, 5)]
resultado4 = formar_times(n4, amizades4)
print(f"Alunos: {n4}")
print(f"Amizades: {amizades4}")
print(f"Times formados: {resultado4}")
print(f"Esperado: 3 (grupo 0-1, grupo 2-3-5, aluno 4 sozinho)")


print("\n\n===== Teste 5 - Grafo Completo =====\n")
n5 = 4
amizades5 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
resultado5 = formar_times(n5, amizades5)
print(f"Alunos: {n5}")
print(f"Amizades: {amizades5}")
print(f"Times formados: {resultado5}")
print(f"Esperado: 1 (todos conectados entre si)")


print("\n\n===== Teste 6 - Representação do Grafo =====\n")
grafo_exemplo = GrafoNaoDirecionado(n1)

for i, j in amizades1:
    grafo_exemplo.adicionar_aresta(i, j)

print(f"Representação: {grafo_exemplo}\n")
