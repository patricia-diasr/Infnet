from typing import Optional


class UnionFind:
    """
    Estrutura de união e busca com compressão de caminho e união por rank

    Attributes:
        _pai (dict): Mapeamento de cada elemento para seu representante atual
        _rank (dict): Altura estimada da árvore de cada representante
    """

    def __init__(self, elementos: list) -> None:
        self._pai: dict = {e: e for e in elementos}
        self._rank: dict = {e: 0 for e in elementos}


    def encontrar(self, x: str) -> str:
        """
        Retorna o representante do conjunto de x com compressão de caminho

        Args:
            x (str): Elemento a ser consultado

        Returns:
            str: Representante canônico do conjunto
        """

        while self._pai[x] != x:
            self._pai[x] = self._pai[self._pai[x]]
            x = self._pai[x]

        return x

    def unir(self, x: str, y: str) -> bool:
        """
        Une os conjuntos de x e y, retornando False se já pertencem ao mesmo conjunto

        Args:
            x (str): Primeiro elemento
            y (str): Segundo elemento

        Returns:
            bool: True se a união foi realizada, False se já eram do mesmo conjunto
        """

        rx, ry = self.encontrar(x), self.encontrar(y)

        if rx == ry:
            return False

        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx

        self._pai[ry] = rx

        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1

        return True


    def mesmo_conjunto(self, x: str, y: str) -> bool:
        """
        Verifica se dois elementos pertencem ao mesmo conjunto

        Args:
            x (str): Primeiro elemento
            y (str): Segundo elemento

        Returns:
            bool: True se pertencem ao mesmo conjunto
        """

        return self.encontrar(x) == self.encontrar(y)


    def __repr__(self) -> str:
        raizes = set(self.encontrar(e) for e in self._pai)
        return f"UnionFind(componentes = {len(raizes)})"


def _extrair_arestas(grafo: dict) -> list:
    """
    Converte o dicionário de adjacência em uma lista de arestas únicas ordenadas por peso

    Args:
        grafo (dict): Mapeamento de cidade para dicionário de vizinhos e distâncias

    Returns:
        list: Lista de tuplas (origem, destino, peso) sem duplicatas, ordenada por peso
    """

    vistas = set()
    arestas = []

    for u, vizinhos in grafo.items():
        for v, peso in vizinhos.items():
            chave = (min(u, v), max(u, v))
            
            if chave not in vistas:
                vistas.add(chave)
                arestas.append((u, v, peso))

    arestas.sort(key=lambda x: x[2])
    return arestas


def _bfs_componente(origem: str, excluir: tuple, adjacencia_mst: dict) -> set:
    """
    Percorre em largura a MST excluindo uma aresta e retorna o componente alcançado a partir de origem

    Args:
        origem (str): Vértice inicial do percurso
        excluir (tuple): Par (u, v) da aresta a ser ignorada durante o percurso
        adjacencia_mst (dict): Lista de adjacência da MST atual

    Returns:
        set: Conjunto de vértices alcançáveis a partir de origem sem usar a aresta excluída
    """

    u_excluir, v_excluir = excluir
    visitados = set()
    fila = [origem]

    while fila:
        atual = fila.pop(0)
        
        if atual in visitados:
            continue
        
        visitados.add(atual)
        
        for viz in adjacencia_mst[atual]:
            ignorar = (atual == u_excluir and viz == v_excluir)
            ignorar = ignorar or (atual == v_excluir and viz == u_excluir)
        
            if viz not in visitados and not ignorar:
                fila.append(viz)

    return visitados


def construir_mst_com_grau(grafo: dict, limite_padrao: int, limites_especiais: dict) -> dict:
    """
    Constrói a árvore geradora mínima respeitando restrições de grau máximo por vértice

    Args:
        grafo (dict): Mapeamento de cidade para dicionário de vizinhos e distâncias
        limite_padrao (int): Grau máximo permitido para a maioria dos vértices
        limites_especiais (dict): Vértices com limites diferentes do padrão

    Returns:
        dict: Dicionário com chaves 'arestas', 'custo_total', 'graus' e 'conectado'
    """

    vertices = list(grafo.keys())
    arestas = _extrair_arestas(grafo)
    limites = {v: limites_especiais.get(v, limite_padrao) for v in vertices}
    graus = {v: 0 for v in vertices}
    uf = UnionFind(vertices)
    mst = []
    custo_total = 0

    for u, v, peso in arestas:

        if uf.mesmo_conjunto(u, v):
            continue
        
        if graus[u] >= limites[u] or graus[v] >= limites[v]:
            continue
        
        uf.unir(u, v)
        graus[u] += 1
        graus[v] += 1
        mst.append((u, v, peso))
        custo_total += peso

    raizes = set(uf.encontrar(v) for v in vertices)
    conectado = len(raizes) == 1

    return {
        "arestas": mst,
        "custo_total": custo_total,
        "graus": graus,
        "limites": limites,
        "conectado": conectado,
    }


def analisar_resiliencia(resultado_mst: dict, grafo: dict) -> dict:
    """
    Identifica a aresta mais crítica da MST e o backup ideal para cada aresta

    Args:
        resultado_mst (dict): Resultado retornado por construir_mst_com_grau
        grafo (dict): Mapeamento de cidade para dicionário de vizinhos e distâncias

    Returns:
        dict: Dicionário com chaves 'analise', 'aresta_critica', 'pontes_absolutas'
    """

    mst = resultado_mst["arestas"]
    vertices = list(grafo.keys())

    arestas_grafo = _extrair_arestas(grafo)
    mst_set = {(min(u, v), max(u, v)) for u, v, _ in mst}
    arestas_fora_mst = [
        (u, v, p) for u, v, p in arestas_grafo
        if (min(u, v), max(u, v)) not in mst_set
    ]
    adjacencia_mst = {v: [] for v in vertices}
    
    for u, v, _ in mst:
        adjacencia_mst[u].append(v)
        adjacencia_mst[v].append(u)

    analise = []
    pontes_absolutas = []

    for u, v, peso in mst:
        comp_u = _bfs_componente(u, (u, v), adjacencia_mst)
        comp_v = set(vertices) - comp_u
        melhor_backup = None
        melhor_peso = float("inf")

        for bu, bv, bp in arestas_fora_mst:
            cruza = (bu in comp_u and bv in comp_v) or (bu in comp_v and bv in comp_u)
            
            if cruza and bp < melhor_peso:
                melhor_peso = bp
                melhor_backup = (bu, bv, bp)

        if melhor_backup is None:
            pontes_absolutas.append((u, v, peso))
            analise.append({
                "aresta": (u, v, peso),
                "backup": None,
                "delta": None,
                "e_ponte_absoluta": True,
            })

        else:
            delta = melhor_backup[2] - peso
            analise.append({
                "aresta": (u, v, peso),
                "backup": melhor_backup,
                "delta": delta,
                "e_ponte_absoluta": False,
            })

    aresta_critica = max(
        (item for item in analise if not item["e_ponte_absoluta"]),
        key = lambda x: x["delta"],
        default = None,
    )

    return {
        "analise": analise,
        "aresta_critica": aresta_critica,
        "pontes_absolutas": pontes_absolutas,
    }


grafo_espanha = {
    "Coruña": {
        "Vigo": 171,
        "Valladolid": 455
    },
    "Vigo": {
        "Coruña": 171,
        "Valladolid": 356
    },
    "Valladolid": {
        "Coruña": 455,
        "Vigo": 356,
        "Bilbao": 280,
        "Madrid": 193
    },
    "Oviedo": {
        "Bilbao": 304
    },
    "Bilbao": {
        "Oviedo": 304,
        "Valladolid": 280,
        "Madrid": 395,
        "Zaragoza": 324
    },
    "Madrid": {
        "Valladolid": 193,
        "Bilbao": 395,
        "Zaragoza": 325,
        "Badajoz": 403,
        "Albacete": 251,
        "Jaén": 335
    },
    "Zaragoza": {
        "Bilbao": 324,
        "Madrid": 325,
        "Barcelona": 296
    },
    "Barcelona": {
        "Zaragoza": 296,
        "Gerona": 100,
        "Valencia": 349
    },
    "Gerona": {
        "Barcelona": 100
    },
    "Badajoz": {
        "Madrid": 403
    },
    "Albacete": {
        "Madrid": 251,
        "Valencia": 191,
        "Murcia": 150
    },
    "Valencia": {
        "Barcelona": 349,
        "Albacete": 191,
        "Murcia": 241
    },
    "Murcia": {
        "Albacete": 150,
        "Valencia": 241,
        "Granada": 278
    },
    "Jaén": {
        "Madrid": 335,
        "Sevilla": 242,
        "Granada": 99
    },
    "Granada": {
        "Jaén": 99,
        "Murcia": 278,
        "Sevilla": 256
    },
    "Sevilla": {
        "Jaén": 242,
        "Granada": 256,
        "Cádiz": 125
    },
    "Cádiz": {
        "Sevilla": 125
    },
}


print("\n===== Teste 1 - Construção da Rede Principal =====\n")

resultado = construir_mst_com_grau(grafo = grafo_espanha, limite_padrao = 3, limites_especiais = {"Madrid": 4},)

print(f"Rede conectada: {resultado['conectado']}")
print(f"Segmentos selecionados: {len(resultado['arestas'])} (esperado: {len(grafo_espanha) - 1})")
print(f"Custo total: {resultado['custo_total']} km\n")
print(f"{'Origem':<15}  {'Destino':<15}  {'Distância':>10}")
print(f"{'-' * 15}  {'-' * 15}  {'-' * 10}")

for u, v, peso in resultado["arestas"]:
    print(f"{u:<15}  {v:<15}  {peso:>10} km")


print("\n\n===== Teste 2 - Graus das Cidades na Rede =====\n")

print(f"{'Cidade':<15}  {'Conexões':>9}  {'Limite':>7}  {'Status':<10}")
print(f"{'-' * 15}  {'-' * 9}  {'-' * 7}  {'-' * 10}")

for cidade in sorted(resultado["graus"]):
    grau = resultado["graus"][cidade]
    limite = resultado["limites"][cidade]
    status = "OK" if grau <= limite else "VIOLADO"
    print(f"{cidade:<15}  {grau:>9}  {limite:>7}  {status:<10}")


print("\n\n===== Teste 3 - Análise de Resiliência =====\n")

resiliencia = analisar_resiliencia(resultado, grafo_espanha)
print("Pontes absolutas (rompimento sem backup possível no mapa):")

if resiliencia["pontes_absolutas"]:
    for u, v, peso in resiliencia["pontes_absolutas"]:
        print(f"  {u} -- {v} ({peso} km): vértice terminal sem rota alternativa")

else:
    print("  Nenhuma")

print(f"\n{'Aresta MST':<35}  {'Peso':>5}  {'Backup disponível':<35}  {'Delta':>7}")
print(f"{'-' * 35}  {'-' * 5}  {'-' * 35}  {'-' * 7}")

for item in resiliencia["analise"]:
    u, v, peso = item["aresta"]
    rotulo = f"{u} -- {v}"

    if item["e_ponte_absoluta"]:
        print(f"{rotulo:<35}  {peso:>5}  {'ponte absoluta (sem backup)':<35}  {'N/A':>7}")

    else:
        bu, bv, bp = item["backup"]
        rotulo_backup = f"{bu} -- {bv}"
        print(f"{rotulo:<35}  {peso:>5}  {rotulo_backup:<35}  {item['delta']:>+7} km")


print("\n\n===== Teste 4 - Aresta Mais Crítica com Backup =====\n")

critica = resiliencia["aresta_critica"]
u, v, peso = critica["aresta"]
bu, bv, bp = critica["backup"]
custo_original = resultado["custo_total"]
custo_com_falha = custo_original - peso + bp

print(f"Aresta mais crítica: {u} -- {v} ({peso} km)")
print(f"Backup recomendado: {bu} -- {bv} ({bp} km)")
print(f"Acréscimo de custo: +{critica['delta']} km")
print(f"Custo original da rede: {custo_original} km")
print(f"Custo após falha e backup: {custo_com_falha} km\n")
