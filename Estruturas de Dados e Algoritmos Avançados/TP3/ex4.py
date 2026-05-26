from typing import List, Dict, Optional


class GrafoProdutos:
    """
    Grafo não direcionado de produtos relacionados representado por lista de adjacência

    Attributes:
        _adjacencia (Dict[str, List[str]]): Mapa de cada produto para seus produtos relacionados
    """

    def __init__(self) -> None:
        self._adjacencia: Dict[str, List[str]] = {}


    def adicionar_produto(self, produto: str) -> None:
        """
        Adiciona um produto ao grafo caso ainda não exista

        Args:
            produto (str): Nome do produto a ser adicionado
        """

        if produto not in self._adjacencia:
            self._adjacencia[produto] = []


    def adicionar_relacao(self, a: str, b: str) -> None:
        """
        Adiciona uma relação de similaridade bidirecional entre dois produtos

        Args:
            a (str): Primeiro produto da relação
            b (str): Segundo produto da relação
        """

        self.adicionar_produto(a)
        self.adicionar_produto(b)
        self._adjacencia[a].append(b)
        self._adjacencia[b].append(a)


    def vizinhos_ordenados(self, produto: str) -> List[str]:
        """
        Retorna os produtos relacionados a um produto em ordem lexicográfica

        Args:
            produto (str): Produto consultado

        Returns:
            List[str]: Lista de produtos relacionados ordenada lexicograficamente
        """

        return sorted(self._adjacencia[produto])


    def produtos(self) -> List[str]:
        """
        Retorna todos os produtos cadastrados no grafo

        Returns:
            List[str]: Lista de produtos
        """

        return list(self._adjacencia.keys())


    def num_produtos(self) -> int:
        """
        Retorna o número total de produtos no grafo

        Returns:
            int: Número de produtos
        """

        return len(self._adjacencia)


    def num_relacoes(self) -> int:
        """
        Retorna o número total de relações de similaridade no grafo

        Returns:
            int: Número de relações
        """

        return sum(len(v) for v in self._adjacencia.values()) // 2


    def __repr__(self) -> str:
        return f"GrafoProdutos(produtos = {self.num_produtos()}, relacoes = {self.num_relacoes()})"


def _dfs_recursiva(grafo: GrafoProdutos, produto: str, visitados: Dict[str, bool], order_visita: List[str], profundidade: int) -> None:
    """
    Percorre o grafo em profundidade a partir de um produto, respeitando ordem lexicográfica dos vizinhos

    Args:
        grafo (GrafoProdutos): Grafo de produtos a ser percorrido
        produto (str): Produto atual do percurso
        visitados (Dict[str, bool]): Mapa de controle de produtos já visitados
        order_visita (List[str]): Lista acumuladora da ordem de visita
        profundidade (int): Profundidade atual no percurso, usada para exibição
    """

    visitados[produto] = True
    order_visita.append(produto)
    print(f"{'  ' * profundidade}visitando: {produto}")

    for vizinho in grafo.vizinhos_ordenados(produto):
        if not visitados.get(vizinho, False):
            _dfs_recursiva(grafo, vizinho, visitados, order_visita, profundidade + 1)


def dfs_recomendacoes(grafo: GrafoProdutos, origem: str) -> List[str]:
    """
    Executa DFS a partir de um produto de origem e retorna a ordem de visita dos produtos

    Args:
        grafo (GrafoProdutos): Grafo de produtos a ser percorrido
        origem (str): Produto inicial da exploração

    Returns:
        List[str]: Sequência de produtos na ordem em que foram descobertos pela DFS
    """

    visitados: Dict[str, bool] = {}
    order_visita: List[str] = []
    _dfs_recursiva(grafo, origem, visitados, order_visita, 0)

    return order_visita


def construir_grafo_produtos() -> GrafoProdutos:
    """
    Constrói o grafo de produtos com as relações de similaridade definidas no enunciado

    Returns:
        GrafoProdutos: Grafo de produtos preenchido com todas as relações
    """

    grafo = GrafoProdutos()
    relacoes = [
        ("brush", "nail_polish"),
        ("nail_polish", "eye_shadow"),
        ("eye_shadow", "eye_glasses"),
        ("nail_polish", "nails"),
        ("nails", "pins"),
        ("nails", "needles"),
        ("pins", "needles"),
        ("nails", "hammer"),
        ("hammer", "drill"),
        ("hammer", "saw"),
        ("saw", "knife"),
        ("knife", "fork"),
        ("knife", "spoon"),
    ]

    for a, b in relacoes:
        grafo.adicionar_relacao(a, b)

    return grafo


print("\n===== Teste 1 - DFS a Partir de Nails com Vizinhos Lexicográficos =====\n")
grafo = construir_grafo_produtos()
print(f"Grafo construído: {grafo}\n")
print("Percurso DFS (recuos indicam profundidade):\n")
ordem = dfs_recomendacoes(grafo, "nails")
print(f"\nOrdem de visita: {ordem}")


print("\n\n===== Teste 2 - Vizinhos Lexicográficos de Cada Produto Visitado =====\n")
print(f"{'Produto':<15}  {'Vizinhos (ordem lexicográfica)'}")
print(f"{'-' * 15}  {'-' * 35}")
for produto in sorted(grafo.produtos()):
    vizinhos = grafo.vizinhos_ordenados(produto)
    print(f"{produto:<15}  {vizinhos}")


print("\n\n===== Teste 3 - DFS a Partir de Outros Vértices =====\n")
origens = ["hammer", "knife", "brush"]

for origem in origens:
    visitados: Dict[str, bool] = {}
    ordem_alt: List[str] = []
    _dfs_recursiva(grafo, origem, visitados, ordem_alt, 0)
    print(f"Origem '{origem}': {ordem_alt}\n")


print("\n===== Teste 4 - Verificação de Cobertura Total do Grafo =====\n")
todos_produtos = set(grafo.produtos())
visitados_final = set(ordem)
nao_visitados = todos_produtos - visitados_final

print(f"Total de produtos no grafo: {grafo.num_produtos()}")
print(f"Produtos visitados pela DFS a partir de 'nails': {len(visitados_final)}")
print(f"Produtos não visitados: {nao_visitados if nao_visitados else 'nenhum'}")
print(f"Grafo é conexo: {len(nao_visitados) == 0}\n")
