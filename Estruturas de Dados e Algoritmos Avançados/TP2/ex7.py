from typing import Dict, List, Set


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


print("\n===== Teste 1 - Construção do grafo =====\n")

g = GraphAdjList()
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
    g.add_edge(u, v)

print(f"Vértices: {sorted(g.adj.keys())}")
print(f"Total de vértices: {len(g.adj)}")
print(f"Total de arestas (não direcionadas): {len(arestas)}\n")


print("\n===== Teste 2 - Lista de adjacência completa =====\n")

for v in sorted(g.adj.keys()):
    print(f"{v}: {sorted(g.adj[v])}")


print("\n\n===== Teste 3 - Validação de simetria (grafo não direcionado) =====\n")

erros = []

for u in g.adj:
    for v in g.adj[u]:
        if u not in g.adj[v]:
            erros.append((u, v))

print(f"Arestas assimétricas encontradas: {erros if erros else 'nenhuma'}")
print(f"Grafo consistente: {len(erros) == 0}\n")


print("\n===== Teste 4 - Adição de vértice isolado =====\n")

g.add_vertex(10)
print(f"Vértice 10 adicionado")
print(f"Vizinhos de 10: {sorted(g.adj[10])}")
print(f"Total de vértices: {len(g.adj)}\n")


print("\n===== Teste 5 - Adição de aresta direcionada =====\n")

g.add_edge(10, 0, directed=True)
print(f"Aresta direcionada 10 -> 0 adicionada")
print(f"Vizinhos de 10: {sorted(g.adj[10])}")
print(f"Vizinhos de 0 (não deve conter 10): {sorted(g.adj[0])}\n")
