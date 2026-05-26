from typing import List, Dict, Tuple
from collections import deque


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


def bfs_recomendacoes(grafo: GrafoProdutos, origem: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Executa BFS a partir de um produto de origem e retorna a ordem de visita e a camada de cada produto

    Args:
        grafo (GrafoProdutos): Grafo de produtos a ser percorrido
        origem (str): Produto inicial da exploração

    Returns:
        Tuple[List[str], Dict[str, int]]: Sequência de produtos na ordem de visita e mapa de produto para sua camada
    """

    visitados: Dict[str, bool] = {origem: True}
    camadas: Dict[str, int] = {origem: 0}
    ordem_visita: List[str] = []
    fila: deque = deque([origem])

    while fila:
        produto = fila.popleft()
        ordem_visita.append(produto)

        for vizinho in grafo.vizinhos_ordenados(produto):
            if vizinho not in visitados:
                visitados[vizinho] = True
                camadas[vizinho] = camadas[produto] + 1
                fila.append(vizinho)

    return ordem_visita, camadas


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


print("\n===== Teste 1 - BFS a Partir de Nails com Vizinhos Lexicográficos =====\n")
grafo = construir_grafo_produtos()
print(f"Grafo construído: {grafo}\n")
ordem_bfs, camadas = bfs_recomendacoes(grafo, "nails")
print(f"{'Posição':<10}  {'Produto':<15}  {'Camada'}")
print(f"{'-' * 10}  {'-' * 15}  {'-' * 6}")

for i, produto in enumerate(ordem_bfs, 1):
    print(f"{i:<10}  {produto:<15}  {camadas[produto]}")


print("\n\n===== Teste 2 - Produtos Agrupados por Camada =====\n")
camadas_agrupadas: Dict[int, List[str]] = {}

for produto, camada in camadas.items():
    if camada not in camadas_agrupadas:
        camadas_agrupadas[camada] = []

    camadas_agrupadas[camada].append(produto)

print(f"{'Camada':<8}  {'Distância':<12}  {'Produtos'}")
print(f"{'-' * 8}  {'-' * 12}  {'-' * 40}")

for camada in sorted(camadas_agrupadas):
    distancia = f"{camada} aresta(s)"
    produtos_camada = sorted(camadas_agrupadas[camada])
    print(f"{camada:<8}  {distancia:<12}  {produtos_camada}")


print("\n\n===== Teste 3 - BFS a Partir de Outros Vértices =====\n")
origens = ["hammer", "knife", "brush"]

for origem in origens:
    ordem_alt, camadas_alt = bfs_recomendacoes(grafo, origem)
    print(f"Origem '{origem}': {ordem_alt}")


print("\n\n===== Teste 4 - Comparação BFS x DFS a Partir de Nails =====\n")
ordem_dfs = ["nails", "hammer", "drill", "saw", "knife", "fork", "spoon", "nail_polish", "brush", "eye_shadow", "eye_glasses", "needles", "pins"]
print(f"{'Posição':<10}  {'BFS':<15}  {'DFS':<15}  {'Mesma ordem'}")
print(f"{'-' * 10}  {'-' * 15}  {'-' * 15}  {'-' * 12}")

for i, (bfs, dfs) in enumerate(zip(ordem_bfs, ordem_dfs), 1):
    mesma = "sim" if bfs == dfs else "não"
    print(f"{i:<10}  {bfs:<15}  {dfs:<15}  {mesma}")

divergencias = sum(1 for b, d in zip(ordem_bfs, ordem_dfs) if b != d)
print(f"\nPosições com ordens diferentes: {divergencias} de {len(ordem_bfs)}")


print("\n\n===== Teste 5 - Verificação de Cobertura Total do Grafo =====\n")
todos_produtos = set(grafo.produtos())
visitados_bfs = set(ordem_bfs)
nao_visitados = todos_produtos - visitados_bfs

print(f"Total de produtos no grafo: {grafo.num_produtos()}")
print(f"Produtos visitados pela BFS a partir de 'nails': {len(visitados_bfs)}")
print(f"Produtos não visitados: {nao_visitados if nao_visitados else 'nenhum'}")
print(f"Grafo é conexo: {len(nao_visitados) == 0}\n")
