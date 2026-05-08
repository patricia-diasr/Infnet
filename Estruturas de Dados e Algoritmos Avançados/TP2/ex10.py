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


    def to_mermaid(self, directed: bool = False) -> str:
        """
        Exporta o grafo como string no formato Mermaid

        Args:
            directed (bool): Se True, usa setas direcionadas (-->), caso contrário usa linhas (---)

        Returns:
            str: String no formato Mermaid representando o grafo
        """

        conector = "-->" if directed else "---"
        linhas = ["graph TD"]
        vistas = set()

        for u in sorted(self.adj.keys()):
            if not self.adj[u]:
                linhas.append(f"  {u}")
                continue

            for v in sorted(self.adj[u]):
                aresta = (min(u, v), max(u, v)) if not directed else (u, v)

                if aresta not in vistas:
                    vistas.add(aresta)
                    linhas.append(f"  {u} {conector} {v}")

        return "\n".join(linhas)


    def __repr__(self) -> str:
        linhas = [f"  {v}: {sorted(vizinhos)}" for v, vizinhos in sorted(self.adj.items())]
        return "GraphAdjList(\n" + "\n".join(linhas) + "\n)"


print("\n===== Teste 1 - Exportação não direcionada =====\n")

g_export = GraphAdjList()
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

for u, v in arestas:
    g_export.add_edge(u, v)

g_export.add_vertex(10)
mermaid_nd = g_export.to_mermaid(directed=False)
print(mermaid_nd)


print("\n\n===== Teste 2 - Contagem de arestas na saída =====\n")

linhas_aresta = [l for l in mermaid_nd.splitlines() if "---" in l]
print(f"Arestas no grafo original: {len(arestas)}")
print(f"Linhas de aresta no Mermaid: {len(linhas_aresta)}")
print(f"Sem duplicatas: {len(linhas_aresta) == len(arestas)}\n")


print("\n===== Teste 3 - Exportação direcionada =====\n")

g_dir = GraphAdjList()
arestas_dir = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]

for u, v in arestas_dir:
    g_dir.add_edge(u, v, directed=True)

mermaid_dir = g_dir.to_mermaid(directed=True)
print(mermaid_dir)


print("\n\n===== Teste 4 - Vértice isolado na saída =====\n")

linhas = mermaid_nd.splitlines()
isolados = [l.strip() for l in linhas if "---" not in l and l.strip().isdigit()]
print(f"Vértices isolados na saída Mermaid: {isolados}")
print(f"Vértice 10 presente: {'10' in isolados}\n")
