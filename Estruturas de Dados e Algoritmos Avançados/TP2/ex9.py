import sys
import time
from typing import Dict, List


class GraphAdjMatrix:
    """
    Grafo representado por matriz de adjacência

    Attributes:
        index (Dict[int, int]): Mapeamento de vértice para índice na matriz
        mat (List[List[int]]): Matriz de adjacência de 0/1
    """

    def __init__(self) -> None:
        self.index: Dict[int, int] = {}
        self.mat: List[List[int]] = []


    def add_vertex(self, v: int) -> None:
        """
        Adiciona um vértice ao grafo, expandindo a matriz, sem efeito se já existir

        Args:
            v (int): Vértice a ser adicionado
        """

        if v in self.index:
            return

        novo_indice = len(self.index)
        self.index[v] = novo_indice

        for linha in self.mat:
            linha.append(0)

        self.mat.append([0] * (novo_indice + 1))


    def add_edge(self, u: int, v: int, directed: bool = False) -> None:
        """
        Adiciona uma aresta entre os vértices u e v, criando os vértices se necessário

        Args:
            u (int): Vértice de origem
            v (int): Vértice de destino
            directed (bool): Se True, cria aresta apenas de u para v
        """

        self.add_vertex(u)
        self.add_vertex(v)
        i, j = self.index[u], self.index[v]
        self.mat[i][j] = 1

        if not directed:
            self.mat[j][i] = 1


    def has_edge(self, u: int, v: int) -> bool:
        """
        Verifica se existe aresta entre os vértices u e v

        Args:
            u (int): Vértice de origem
            v (int): Vértice de destino

        Returns:
            bool: True se existir aresta de u para v, False caso contrário

        Raises:
            KeyError: Se u ou v não existirem no grafo
        """

        i, j = self.index[u], self.index[v]
        return self.mat[i][j] == 1


    def __repr__(self) -> str:
        vertices = sorted(self.index.keys(), key=lambda v: self.index[v])
        cabecalho = "     " + "  ".join(f"{v:2}" for v in vertices)
        linhas = [cabecalho]

        for v in vertices:
            linha = self.mat[self.index[v]]
            linhas.append(f"{v:3}: " + "  ".join(f"{x:2}" for x in linha))

        return "\n".join(linhas)


class GraphAdjList:
    """
    Grafo representado por lista de adjacência

    Attributes:
        adj (Dict[int, Set[int]]): Mapeamento de vértice para conjunto de vizinhos
    """

    def __init__(self) -> None:
        self.adj: Dict[int, Set[int]] = {}


    def add_vertex(self, v: int) -> None:
        """
        Adiciona um vértice ao grafo, sem efeito se já existir

        Args:
            v (int): Vértice a ser adicionado
        """

        if v not in self.adj:
            self.adj[v] = set()


    def add_edge(self, u: int, v: int, directed: bool = False) -> None:
        """
        Adiciona uma aresta entre os vértices u e v, criando os vértices se necessário

        Args:
            u (int): Vértice de origem
            v (int): Vértice de destino
            directed (bool): Se True, cria aresta apenas de u para v
        """

        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].add(v)

        if not directed:
            self.adj[v].add(u)


    def __repr__(self) -> str:
        linhas = [f"  {v}: {sorted(vizinhos)}" for v, vizinhos in sorted(self.adj.items())]
        return "GraphAdjList(\n" + "\n".join(linhas) + "\n)"


print("\n===== Teste 1 - Vértices nas duas representações =====\n")

g_lista = GraphAdjList()
g_matriz = GraphAdjMatrix()

vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
arestas = [
    (0, 1), (0, 2), (0, 3),
    (1, 4), (1, 5),
    (2, 5), (2, 6),
    (3, 7),
    (4, 8),
    (5, 9),
    (6, 9),
    (7, 8),
]

for v in vertices:
    g_lista.add_vertex(v)
    g_matriz.add_vertex(v)

for u, v in arestas:
    g_lista.add_edge(u, v)
    g_matriz.add_edge(u, v)

print("Lista de adjacência - chaves do dicionário adj (vértices):")
print(f"=> {sorted(g_lista.adj.keys())}")

print("\nMatriz de adjacência - chaves do dicionário index (vértices -> índices):")
print(f"=> {dict(sorted(g_matriz.index.items()))}\n")


print("\n===== Teste 2 - Arestas nas duas representações =====\n")

aresta_demo = (0, 1)
u, v = aresta_demo

print(f"Aresta de demonstração: {u} - {v}")
print(f"Lista: g_lista.adj[{u}] = {sorted(g_lista.adj[u])}")
print(f"=> vértice {v} presente na lista de {u}: {v in g_lista.adj[u]}")
print(f"Lista: g_lista.adj[{v}] = {sorted(g_lista.adj[v])}")
print(f"=> vértice {u} presente na lista de {v}: {u in g_lista.adj[v]}")

i, j = g_matriz.index[u], g_matriz.index[v]
print(f"\nMatriz: index[{u}]={i}, index[{v}]={j}")
print(f"=> mat[{i}][{j}] = {g_matriz.mat[i][j]}")
print(f"=> mat[{j}][{i}] = {g_matriz.mat[j][i]}\n")


print("\n===== Teste 3 - Estrutura completa da lista de adjacência =====\n")

for v in sorted(g_lista.adj.keys()):
    print(f"{v}: {sorted(g_lista.adj[v])}")


print("\n\n===== Teste 4 - Estrutura completa da matriz de adjacência =====\n")

print(g_matriz)


print("\n\n===== Teste 5 - Consulta has_edge nas duas representações =====\n")

consultas = [(0, 1), (0, 9), (3, 5), (7, 8), (2, 6)]
repeticoes = 100_000

print(f"{'(u,v)':<8}  {'lista':>6}  {'matriz':>7}  {'t_lista (ms)':>13}  {'t_matriz (ms)':>13}")
print(f"{'-'*8}  {'-'*6}  {'-'*7}  {'-'*13}  {'-'*13}")

for u, v in consultas:
    inicio = time.perf_counter()

    for _ in range(repeticoes):
        _ = v in g_lista.adj[u]

    t_lista = (time.perf_counter() - inicio) * 1000
    inicio = time.perf_counter()

    for _ in range(repeticoes):
        _ = g_matriz.has_edge(u, v)
    
    t_matriz = (time.perf_counter() - inicio) * 1000
    res_lista = v in g_lista.adj[u]
    res_matriz = g_matriz.has_edge(u, v)
    print(f"({u},{v}){'':3}  {str(res_lista):>6}  {str(res_matriz):>7}  {t_lista:>13.3f}  {t_matriz:>13.3f}")

print(f"\n(médias sobre {repeticoes} repetições por consulta)\n")


print("\n===== Teste 6 - Custo de memória das duas representações =====\n")

n = len(vertices)
e = len(arestas)

tam_adj = sys.getsizeof(g_lista.adj) + sum(sys.getsizeof(s) for s in g_lista.adj.values())
tam_mat = sys.getsizeof(g_matriz.mat) + sum(sys.getsizeof(linha) for linha in g_matriz.mat) + sys.getsizeof(g_matriz.index)

print(f"Vértices: {n}, Arestas: {e}")
print(f"Tamanho da lista de adjacência: {tam_adj} bytes")
print(f"Tamanho da matriz de adjacência: {tam_mat} bytes")
print(f"Células úteis na matriz (arestas x2): {e * 2}")
print(f"Células totais na matriz: {n * n}")
print(f"Taxa de ocupação da matriz: {(e * 2) / (n * n) * 100:.1f}%\n")
