from typing import Optional


class GrafoDirecionado:
    """
    Grafo direcionado baseado em lista de adjacência para modelagem de dependências

    Attributes:
        _adjacencia (dict): Mapeamento de cada vértice para sua lista de vizinhos downstream
        _vertices (set): Conjunto de todos os vértices registrados no grafo
    """

    def __init__(self) -> None:
        self._adjacencia: dict = {}
        self._vertices: set = set()


    def adicionar_vertice(self, vertice: str) -> None:
        """
        Registra um vértice no grafo sem adicionar arestas

        Args:
            vertice (str): Identificador do microsserviço
        """

        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = []
        self._vertices.add(vertice)


    def adicionar_aresta(self, origem: str, destino: str) -> None:
        """
        Adiciona uma aresta direcionada de origem para destino, criando os vértices se necessário

        Args:
            origem (str): Serviço que depende do destino
            destino (str): Serviço do qual a origem depende
        """

        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        self._adjacencia[origem].append(destino)


    def vizinhos(self, vertice: str) -> list:
        """
        Retorna a lista de vizinhos downstream de um vértice

        Args:
            vertice (str): Vértice a ser consultado

        Returns:
            list: Lista de vértices para os quais o vértice aponta
        """

        return self._adjacencia.get(vertice, [])


    def vertices(self) -> list:
        """
        Retorna todos os vértices do grafo em ordem de inserção

        Returns:
            list: Lista de identificadores de vértices
        """

        return list(self._adjacencia.keys())


    @classmethod
    def de_dicionario(cls, dicionario: dict) -> "GrafoDirecionado":
        """
        Constrói um GrafoDirecionado a partir de um dicionário de listas de adjacência

        Args:
            dicionario (dict): Mapeamento de vértice para lista de vizinhos downstream

        Returns:
            GrafoDirecionado: Instância construída com todos os vértices e arestas do dicionário
        """

        grafo = cls()

        for origem, destinos in dicionario.items():
            grafo.adicionar_vertice(origem)

            for destino in destinos:
                grafo.adicionar_aresta(origem, destino)

        return grafo


    def __repr__(self) -> str:
        return f"GrafoDirecionado(vertices = {len(self._adjacencia)}, arestas = {sum(len(v) for v in self._adjacencia.values())})"


def mapear_raio_falha_bfs(grafo: GrafoDirecionado, no_inicial: str) -> list:
    """
    Mapeia a propagação de falha por raio de proximidade usando busca em largura

    Args:
        grafo (GrafoDirecionado): Grafo de dependências entre microsserviços
        no_inicial (str): Identificador do microsserviço que originou a falha

    Returns:
        list: Lista de dicionários com chaves 'servico' e 'distancia', na ordem de visitação BFS
    """

    visitados = {no_inicial}
    fila = [(no_inicial, 0)]
    resultado = []
    cabeca = 0

    while cabeca < len(fila):
        no_atual, distancia = fila[cabeca]
        cabeca += 1
        resultado.append({"servico": no_atual, "distancia": distancia})

        for vizinho in grafo.vizinhos(no_atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, distancia + 1))

    return resultado


def encontrar_cadeia_profunda_dfs(grafo: GrafoDirecionado, no_inicial: str) -> list:
    """
    Encontra o caminho linear mais profundo percorrido antes do primeiro backtrack na DFS

    Args:
        grafo (GrafoDirecionado): Grafo de dependências entre microsserviços
        no_inicial (str): Identificador do microsserviço que originou a falha

    Returns:
        list: Lista de identificadores de serviços na ordem do caminho até a primeira folha
    """

    caminho_atual = []
    caminho_final = []
    encontrou_backtrack = [False]

    def _dfs(no: str, visitados: set) -> None:
        if encontrou_backtrack[0]:
            return

        caminho_atual.append(no)
        visitados.add(no)
        filhos_nao_visitados = [v for v in grafo.vizinhos(no) if v not in visitados]

        if not filhos_nao_visitados:
            caminho_final.extend(caminho_atual)
            encontrou_backtrack[0] = True
            return

        for filho in filhos_nao_visitados:
            if encontrou_backtrack[0]:
                return

            _dfs(filho, visitados)

        if not encontrou_backtrack[0]:
            caminho_atual.pop()

    _dfs(no_inicial, set())
    return caminho_final


rede_microsservicos = {
    "Auth": ["Gateway", "Billing"],
    "Gateway": ["Frontend", "MobileApp"],
    "Billing": ["Notification", "Analytics"],
    "Frontend": ["CacheUI"],
    "MobileApp": ["CacheUI", "Logger"],
    "Notification": ["Logger"],
    "Analytics": [],
    "CacheUI": [],
    "Logger": [],
}
grafo = GrafoDirecionado.de_dicionario(rede_microsservicos)


print("\n===== Teste 1 - Estado do Grafo =====\n")
print(f"Representacao: {grafo}")
print(f"Vertices: {grafo.vertices()}")
print()
print(f"{'Serviço':<15}  {'Depende de (downstream)'}")
print(f"{'-' * 15}  {'-' * 40}")

for vertice in grafo.vertices():
    vizinhos = grafo.vizinhos(vertice)
    deps = ", ".join(vizinhos) if vizinhos else "(nenhum)"
    print(f"{vertice:<15}  {deps}")


print("\n\n===== Teste 2 - Raio de Falha BFS a partir de Auth =====\n")

raio = mapear_raio_falha_bfs(grafo, "Auth")
distancia_atual = -1

for entrada in raio:
    if entrada["distancia"] != distancia_atual:
        distancia_atual = entrada["distancia"]
        rotulo = "origem" if distancia_atual == 0 else f"distância {distancia_atual}"
        print(f"  [{rotulo}]")

    print(f"    {entrada['servico']}")

print()
print(f"Ordem completa de isolamento: {[e['servico'] for e in raio]}")


print("\n\n===== Teste 3 - Cadeia Profunda DFS a partir de Auth =====\n")

cadeia = encontrar_cadeia_profunda_dfs(grafo, "Auth")
print(f"Cadeia de colapso em sequência (antes do primeiro backtrack):")

for i, servico in enumerate(cadeia):
    conector = " -> " if i < len(cadeia) - 1 else " -> [falha encerrada aqui]"
    print(f"  {servico}{conector}")

print()
print(f"Profundidade da cadeia: {len(cadeia)} serviços")
print(f"Caminho: {' -> '.join(cadeia)}")


print("\n\n===== Teste 4 - BFS e DFS a partir de outros nós =====\n")

nos_teste = ["Gateway", "Billing", "Analytics"]

for no in nos_teste:
    raio_local = mapear_raio_falha_bfs(grafo, no)
    cadeia_local = encontrar_cadeia_profunda_dfs(grafo, no)
    afetados = [e["servico"] for e in raio_local if e["distancia"] > 0]
    print(f"Falha em '{no}':")
    print(f"  Serviços afetados (BFS): {afetados if afetados else ['nenhum']}")
    print(f"  Cadeia profunda (DFS): {' -> '.join(cadeia_local)}")
    print()


print("\n===== Teste 5 - Nó Sem Dependências (folha) =====\n")

for no_folha in ["CacheUI", "Logger", "Analytics"]:
    raio_local = mapear_raio_falha_bfs(grafo, no_folha)
    cadeia_local = encontrar_cadeia_profunda_dfs(grafo, no_folha)
    print(f"Falha em '{no_folha}' (serviço sem dependentes downstream):")
    print(f"  BFS retorna apenas a origem: {[e['servico'] for e in raio_local]}")
    print(f"  DFS retorna apenas a origem: {cadeia_local}")
    print()
