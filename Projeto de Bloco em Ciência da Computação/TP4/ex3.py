from typing import Dict, List, Optional, Set, Tuple
from collections import deque


class Grafo:
    """
    Grafo direcionado representado por lista de adjacência

    Attributes:
        _adjacencia (Dict[int, List[int]]): Mapeamento de cada vértice para seus vizinhos
        _vertices (Set[int]): Conjunto de todos os vértices registrados no grafo
    """

    def __init__(self) -> None:
        self._adjacencia: Dict[int, List[int]] = {}
        self._vertices: Set[int] = set()


    def adicionar_vertice(self, vertice: int) -> None:
        """
        Registra um vértice no grafo sem arestas associadas

        Args:
            vertice (int): Identificador do vértice a ser adicionado
        """

        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = []

        self._vertices.add(vertice)


    def adicionar_aresta(self, origem: int, destino: int) -> None:
        """
        Adiciona uma aresta direcionada entre dois vértices, criando-os se necessário

        Args:
            origem (int): Vértice de partida da aresta
            destino (int): Vértice de chegada da aresta
        """

        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)

        if destino not in self._adjacencia[origem]:
            self._adjacencia[origem].append(destino)


    def vizinhos(self, vertice: int) -> List[int]:
        """
        Retorna os vizinhos acessíveis a partir de um vértice

        Args:
            vertice (int): Vértice consultado

        Returns:
            List[int]: Lista de vértices alcançáveis diretamente
        """

        return self._adjacencia.get(vertice, [])


    def vertices(self) -> Set[int]:
        """
        Retorna o conjunto de todos os vértices do grafo

        Returns:
            Set[int]: Conjunto de identificadores de vértices
        """

        return set(self._vertices)


    def tamanho(self) -> Tuple[int, int]:
        """
        Retorna o número de vértices e arestas do grafo

        Returns:
            Tuple[int, int]: Par (quantidade de vértices, quantidade de arestas)
        """

        total_arestas = sum(len(vizinhos) for vizinhos in self._adjacencia.values())
        return len(self._vertices), total_arestas


    def para_mermaid(self, caminho: Optional[List[int]] = None, titulo: str = "Labirinto", inicio: Optional[int] = None, saida: Optional[int] = None) -> str:
        """
        Gera uma representação Mermaid do grafo.

        Args:
            caminho (Optional[List[int]]): Caminho a ser destacado
            titulo (str): Título do diagrama
            inicio (Optional[int]): Nó inicial
            saida (Optional[int]): Nó de saída

        Returns:
            str: Código Mermaid
        """

        caminho = caminho or []
        arestas_caminho = set()

        for i in range(len(caminho) - 1):
            arestas_caminho.add((caminho[i], caminho[i + 1]))

        linhas = ["---", f"title: {titulo}", "---", "flowchart TD"]

        for vertice in sorted(self._vertices):
            classes = []

            if vertice == inicio:
                classes.append("inicio")

            if vertice == saida:
                classes.append("saida")

            if vertice in caminho:
                classes.append("caminho")

            linhas.append(f"    {vertice}[\"{vertice}\"]")

            for classe in classes:
                linhas.append(f"    class {vertice} {classe}")

        for origem in sorted(self._adjacencia):
            for destino in self._adjacencia[origem]:
                if (origem, destino) in arestas_caminho:
                    linhas.append(f"    {origem} ==> {destino}")

                else:
                    linhas.append(f"    {origem} --> {destino}")

        linhas.extend([
            "",
            "    classDef caminho fill:#87CEFA,stroke:#1E90FF,stroke-width:3px;",
            "    classDef inicio fill:#90EE90,stroke:#008000,stroke-width:3px;",
            "    classDef saida fill:#FFCCCB,stroke:#FF0000,stroke-width:3px;"
        ])

        return "\n".join(linhas)


    def __repr__(self) -> str:
        v, a = self.tamanho()
        return f"Grafo(vértices = {v}, arestas = {a})"


def dfs(grafo: Grafo, inicio: int, destino: int) -> Optional[List[int]]:
    """
    Busca em profundidade (DFS) para encontrar um caminho entre dois vértices

    Args:
        grafo (Grafo): Grafo sobre o qual a busca será realizada
        inicio (int): Vértice de partida
        destino (int): Vértice de chegada desejado

    Returns:
        Optional[List[int]]: Lista de vértices que forma o caminho do início ao destino, ou None se não houver caminho
    """

    pilha: List[Tuple[int, List[int]]] = [(inicio, [inicio])]
    visitados: Set[int] = set()

    while pilha:
        vertice, caminho = pilha.pop()

        if vertice == destino:
            return caminho

        if vertice in visitados:
            continue

        visitados.add(vertice)

        for vizinho in reversed(grafo.vizinhos(vertice)):
            if vizinho not in visitados:
                pilha.append((vizinho, caminho + [vizinho]))

    return None


def bfs(grafo: Grafo, inicio: int, destino: int) -> Optional[List[int]]:
    """
    Busca em largura (BFS) para encontrar o caminho mais curto entre dois vértices

    Args:
        grafo (Grafo): Grafo sobre o qual a busca será realizada
        inicio (int): Vértice de partida
        destino (int): Vértice de chegada desejado

    Returns:
        Optional[List[int]]: Lista de vértices que forma o caminho mais curto, ou None se não houver caminho
    """

    fila: deque[Tuple[int, List[int]]] = deque()
    fila.append((inicio, [inicio]))
    visitados: Set[int] = {inicio}

    while fila:
        vertice, caminho = fila.popleft()

        if vertice == destino:
            return caminho

        for vizinho in grafo.vizinhos(vertice):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))

    return None


def reconstruir_labirinto() -> Grafo:
    """
    Constrói o grafo do labirinto a partir do mapeamento de vértices e arestas

    Returns:
        Grafo: Grafo direcionado representando o labirinto completo
    """

    arestas = [
        (1, 2), (1, 11), (2, 3), (2, 4), (4, 5), (4, 6), (6, 7), (6, 8), (8, 9), (8, 10),
        (11, 12), (11, 13), (13, 14), (13, 93), (14, 15), (14, 20), (15, 16), (15, 17), (17, 18), (17, 19),
        (20, 21), (20, 22), (22, 23), (22, 80), (23, 24), (23, 25), (25, 26), (25, 79), (26, 27), (26, 28),
        (28, 29), (28, 30), (30, 31), (30, 34), (31, 32), (31, 33), (34, 35), (34, 36), (36, 37), (36, 38),
        (38, 39), (38, 40), (40, 41), (40, 42), (42, 43), (42, 44), (44, 45), (44, 48), (45, 46), (45, 47),
        (48, 49), (48, 50), (50, 51), (50, 54), (51, 52), (51, 53), (54, 55), (54, 62), (55, 56), (55, 59), 
        (56, 57), (56, 58), (59, 60), (59, 61), (62, 63), (62, 74), (63, 64), (63, 65), (65, 66), (65, 67),
        (67, 68), (67, 71), (68, 69), (68, 70), (71, 72), (71, 73), (74, 75), (74, 76), (76, 77), (76, 78),
        (80, 81), (80, 82), (82, 83), (82, 84), (84, 85), (84, 86), (86, 87), (86, 88), (88, 89), (88, 90),
        (90, 91), (90, 92), (93, 94), (93, 95), (93, 96)
    ]

    becos_sem_saida = {3, 5, 7, 9, 10, 12, 16, 18, 19, 21, 24, 27, 29, 32, 33, 35, 37, 39, 43, 46, 47, 49, 52, 53, 57, 58, 60, 61, 64, 66, 69, 70, 73, 75, 77, 78, 79, 81, 83, 85, 87, 89, 91, 92, 94, 95, 96}

    grafo = Grafo()

    for origem, destino in arestas:
        grafo.adicionar_aresta(origem, destino)

    for beco in becos_sem_saida:
        grafo.adicionar_vertice(beco)

    return grafo


def exibir_caminho(caminho: Optional[List[int]], algoritmo: str) -> None:
    """
    Exibe o caminho encontrado em formato legível com separadores visuais

    Args:
        caminho (Optional[List[int]]): Lista de vértices do caminho, ou None se não encontrado
        algoritmo (str): Nome do algoritmo que gerou o caminho
    """

    print(f"Algoritmo: {algoritmo}")

    if caminho is None:
        print("Nenhum caminho encontrado")
        return

    print(f"Comprimento: {len(caminho)} vértices, {len(caminho) - 1} arestas")
    print(f"Caminho: {' -> '.join(str(v) for v in caminho)}")


def exibir_tabela_comparativa(caminho_dfs: Optional[List[int]], caminho_bfs: Optional[List[int]]) -> None:
    """
    Exibe uma tabela comparando os resultados dos dois algoritmos de busca

    Args:
        caminho_dfs (Optional[List[int]]): Caminho encontrado pela DFS
        caminho_bfs (Optional[List[int]]): Caminho encontrado pela BFS
    """

    col_metrica = 24
    col_dfs = 20
    col_bfs = 20

    separador = f"+{'-' * (col_metrica + 2)}+{'-' * (col_dfs + 2)}+{'-' * (col_bfs + 2)}+"
    cabecalho = (
        f"| {'Métrica':^{col_metrica}} "
        f"| {'DFS':^{col_dfs}} "
        f"| {'BFS':^{col_bfs}} |"
    )

    def vertices(c: Optional[List[int]]) -> str:
        return str(len(c)) if c else "não encontrado"

    def arestas(c: Optional[List[int]]) -> str:
        return str(len(c) - 1) if c else "não encontrado"

    print(separador)
    print(cabecalho)
    print(separador)
    print(f"| {'Vértices no caminho':^{col_metrica}} | {vertices(caminho_dfs):^{col_dfs}} | {vertices(caminho_bfs):^{col_bfs}} |")
    print(f"| {'Arestas percorridas':^{col_metrica}} | {arestas(caminho_dfs):^{col_dfs}} | {arestas(caminho_bfs):^{col_bfs}} |")
    print(separador)


labirinto = reconstruir_labirinto()
INICIO = 1
SAIDA  = 41


print("\n===== Teste 1 - Estrutura do Grafo =====\n")
v, a = labirinto.tamanho()
print(f"Vértices: {v}")
print(f"Arestas: {a}")
print(f"Representação: {labirinto}")
print(f"Mermaid:")
print(labirinto.para_mermaid(titulo="Labirinto", inicio=INICIO, saida=SAIDA))


print("\n\n===== Teste 2 - Busca DFS =====\n")
caminho_dfs = dfs(labirinto, INICIO, SAIDA)
exibir_caminho(caminho_dfs, "DFS (Depth-First Search)")
print(f"Mermaid:")
print(labirinto.para_mermaid(caminho=caminho_dfs, titulo="Labirinto - Caminho DFS", inicio=INICIO, saida=SAIDA))


print("\n\n===== Teste 3 - Busca BFS =====\n")
caminho_bfs = bfs(labirinto, INICIO, SAIDA)
exibir_caminho(caminho_bfs, "BFS (Breadth-First Search)")
print(f"Mermaid:")
print(labirinto.para_mermaid(caminho=caminho_bfs, titulo="Labirinto - Caminho BFS", inicio=INICIO, saida=SAIDA))


print("\n\n===== Teste 4 - Tabela Comparativa =====\n")
exibir_tabela_comparativa(caminho_dfs, caminho_bfs)


print("\n\n===== Teste 5 - Verificação dos Caminhos =====\n")

for nome, caminho in [("DFS", caminho_dfs), ("BFS", caminho_bfs)]:
    if caminho is None:
        print(f"{nome}: caminho não encontrado, verificação ignorada")
        continue

    inicio_correto = caminho[0] == INICIO
    fim_correto = caminho[-1] == SAIDA

    arestas_validas = all(
        caminho[i + 1] in labirinto.vizinhos(caminho[i])
        for i in range(len(caminho) - 1)
    )

    sem_repeticao = len(caminho) == len(set(caminho))

    status = "VALIDO" if all([inicio_correto, fim_correto, arestas_validas, sem_repeticao]) else "INVALIDO"

    print(f"{nome}: {status}")
    print(f"Início correto: {inicio_correto}")
    print(f"Fim correto: {fim_correto}")
    print(f"Arestas válidas: {arestas_validas}")
    print(f"Sem repetição: {sem_repeticao}")
    print()
