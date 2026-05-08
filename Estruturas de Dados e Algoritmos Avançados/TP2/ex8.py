import sys
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


print("\n===== Teste 1 - Construção do mesmo grafo do Exercício 7 =====\n")

gm = GraphAdjMatrix()
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
    gm.add_edge(u, v)

print(f"Vértices: {sorted(gm.index.keys())}")
print(f"Total de vértices: {len(gm.index)}")
print(f"Total de arestas (não direcionadas): {len(arestas)}\n")


print("\n===== Teste 2 - Matriz de adjacência completa =====\n")

print(gm)


print("\n\n===== Teste 3 - Consulta has_edge =====\n")

consultas = [(0, 1), (0, 9), (5, 9), (3, 5), (7, 8)]

print(f"{'(u, v)':<10}  {'has_edge':>8}")
print(f"{'-'*10}  {'-'*8}")

for u, v in consultas:
    print(f"({u}, {v}){'':6}  {str(gm.has_edge(u, v)):>8}")


print("\n\n===== Teste 4 - Validação de simetria =====\n")

n = len(gm.index)
erros = []

for u in gm.index:
    for v in gm.index:
        if gm.mat[gm.index[u]][gm.index[v]] != gm.mat[gm.index[v]][gm.index[u]]:
            erros.append((u, v))

print(f"Arestas assimétricas encontradas: {erros if erros else 'nenhuma'}")
print(f"Matriz consistente: {len(erros) == 0}\n")


print("\n===== Teste 5 - Comparação de memória e custo de consulta =====\n")

g = GraphAdjList()

for u, v in arestas:
    g.add_edge(u, v)

vertices = sorted(gm.index.keys())
n = len(vertices)
tamanho_matriz = sys.getsizeof(gm.mat) + sum(sys.getsizeof(linha) for linha in gm.mat)
tamanho_index = sys.getsizeof(gm.index)
total_matriz = tamanho_matriz + tamanho_index

print(f"Vértices: {n}, Arestas: {len(arestas)}")
print(f"\nMatriz de adjacência:")
print(f"=> Células alocadas: {n} x {n} = {n * n}")
print(f"=> Tamanho estimado (mat + index): {total_matriz} bytes")
print(f"\nLista de adjacência:")
print(f"=> Entradas armazenadas: {sum(len(v) for v in g.adj.values())} (2 x arestas, não direcionado)")
print(f"\nCusto de has_edge:")
print(f"=> Matriz: O(1) - acesso direto por índice")
print(f"=> Lista: O(grau(v)) - busca no conjunto de vizinhos, O(1) com set\n")
