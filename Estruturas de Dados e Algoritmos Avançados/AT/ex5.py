from typing import Optional
import math


class GrafoPonderadoDirecionado:
    """
    Grafo direcionado e ponderado baseado em lista de adjacência

    Attributes:
        _adjacencia (dict): Mapeamento de cada vértice para lista de tuplas (vizinho, peso)
        _vertices (list): Vértices na ordem de inserção
    """

    def __init__(self, vertices: list) -> None:
        self._adjacencia: dict = {v: [] for v in vertices}
        self._vertices: list = list(vertices)


    def adicionar_aresta(self, origem: str, destino: str, peso: int) -> None:
        """
        Adiciona uma aresta direcionada com peso

        Args:
            origem (str): Vértice de partida
            destino (str): Vértice de chegada
            peso (int): Tempo estimado em minutos
        """

        self._adjacencia[origem].append((destino, peso))


    def vizinhos(self, vertice: str) -> list:
        """
        Retorna a lista de tuplas (vizinho, peso) a partir de um vértice

        Args:
            vertice (str): Vértice de consulta

        Returns:
            list: Lista de tuplas (destino, peso)
        """

        return self._adjacencia.get(vertice, [])


    def vertices(self) -> list:
        """
        Retorna todos os vértices do grafo

        Returns:
            list: Lista de identificadores de vértices
        """

        return list(self._vertices)


    def __repr__(self) -> str:
        total_arestas = sum(len(v) for v in self._adjacencia.values())
        return f"GrafoPonderadoDirecionado(vertices = {len(self._vertices)}, arestas = {total_arestas})"


class EntregaDia:
    """
    Representa uma entrega a ser realizada durante o turno

    Attributes:
        bairro (str): Nome do bairro de destino
        janela_inicio (int): Minutos desde 09:00 em que a janela abre
        janela_fim (int): Minutos desde 09:00 em que a janela fecha
        prioridade (int): Importância da entrega (maior é mais urgente)
        concluida (bool): Indica se a entrega já foi realizada
    """

    def __init__(self, bairro: str, janela_inicio: int, janela_fim: int, prioridade: int) -> None:
        self.bairro: str = bairro
        self.janela_inicio: int = janela_inicio
        self.janela_fim: int = janela_fim
        self.prioridade: int = prioridade
        self.concluida: bool = False


    def __repr__(self) -> str:
        return (f"EntregaDia(bairro = {self.bairro!r}, janela = [{self.janela_inicio},{self.janela_fim}], prioridade = {self.prioridade}, concluida = {self.concluida})")


class HeapMinima:
    """
    Heap mínima genérica baseada em vetor para seleção de candidatos por score

    Attributes:
        _dados (list): Vetor interno de itens armazenados
        _tamanho (int): Número de itens válidos atualmente na heap
    """

    def __init__(self) -> None:
        self._dados: list = []
        self._tamanho: int = 0


    def _pai(self, i: int) -> int:
        return (i - 1) // 2


    def _filho_esq(self, i: int) -> int:
        return 2 * i + 1


    def _filho_dir(self, i: int) -> int:
        return 2 * i + 2


    def _trocar(self, i: int, j: int) -> None:
        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]


    def _subir(self, i: int) -> None:
        while i > 0:
            pai = self._pai(i)

            if self._dados[i] < self._dados[pai]:
                self._trocar(i, pai)
                i = pai

            else:
                break


    def _descer(self, i: int) -> None:
        while True:
            menor = i
            esq = self._filho_esq(i)
            dir = self._filho_dir(i)

            if esq < self._tamanho and self._dados[esq] < self._dados[menor]:
                menor = esq

            if dir < self._tamanho and self._dados[dir] < self._dados[menor]:
                menor = dir

            if menor != i:
                self._trocar(i, menor)
                i = menor

            else:
                break


    def inserir(self, item: tuple) -> None:
        """
        Insere um item na heap

        Args:
            item (tuple): Tupla comparável usada como chave de prioridade
        """

        if self._tamanho < len(self._dados):
            self._dados[self._tamanho] = item

        else:
            self._dados.append(item)

        self._tamanho += 1
        self._subir(self._tamanho - 1)


    def extrair_minimo(self) -> tuple:
        """
        Remove e retorna o item com menor valor da heap

        Returns:
            tuple: Item com menor prioridade

        Raises:
            IndexError: Se a heap estiver vazia
        """

        if self._tamanho == 0:
            raise IndexError("Heap vazia")

        self._trocar(0, self._tamanho - 1)
        self._tamanho -= 1
        item = self._dados[self._tamanho]

        if self._tamanho > 0:
            self._descer(0)

        return item


    def vazia(self) -> bool:
        """
        Verifica se a heap não contém itens

        Returns:
            bool: True se vazia
        """

        return self._tamanho == 0


    def __repr__(self) -> str:
        return f"HeapMinima(tamanho = {self._tamanho})"


def _floyd_warshall(grafo: GrafoPonderadoDirecionado) -> tuple:
    """
    Calcula os menores caminhos entre todos os pares de vértices

    Args:
        grafo (GrafoPonderadoDirecionado): Grafo de entrada

    Returns:
        tuple: Par (dist, prev) onde dist[i][j] é o custo mínimo e prev[i][j] é o índice do predecessor de j no caminho mínimo de i para j
    """

    vertices = grafo.vertices()
    n = len(vertices)
    indice = {v: i for i, v in enumerate(vertices)}
    INF = math.inf

    dist = [[INF] * n for _ in range(n)]
    prev = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0
        prev[i][i] = i

    for u in vertices:
        for v, peso in grafo.vizinhos(u):
            i, j = indice[u], indice[v]
            dist[i][j] = peso
            prev[i][j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                novo = dist[i][k] + dist[k][j]

                if novo < dist[i][j]:
                    dist[i][j] = novo
                    prev[i][j] = prev[k][j]

    return dist, prev, indice, vertices


def _reconstruir_caminho(prev: list, indice: dict, vertices: list, origem: str, destino: str) -> Optional[list]:
    """
    Reconstrói o caminho mínimo entre dois vértices a partir da tabela de predecessores

    Args:
        prev (list): Tabela de predecessores gerada pelo Floyd-Warshall
        indice (dict): Mapeamento de nome de vértice para índice
        vertices (list): Lista de nomes de vértices
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        Optional[list]: Lista de vértices do caminho, ou None se não houver caminho
    """

    i, j = indice[origem], indice[destino]

    if prev[i][j] is None:
        return None

    caminho = []
    atual = j

    while atual != i:
        caminho.append(vertices[atual])
        proximo = prev[i][atual]

        if proximo is None:
            return None
        
        atual = proximo

    caminho.append(vertices[i])
    caminho.reverse()
    return caminho


class RoteadorEntregas:
    """
    Roteador de entregas que combina Floyd-Warshall com heurística gulosa baseada em heap

    Attributes:
        _grafo (GrafoPonderadoDirecionado): Grafo de bairros e tempos
        _dist (list): Tabela de custos mínimos entre todos os pares
        _prev (list): Tabela de predecessores para reconstrução de caminhos
        _indice (dict): Mapeamento de nome de vértice para índice
        _vertices (list): Lista de nomes de vértices
    """

    def __init__(self, grafo: GrafoPonderadoDirecionado) -> None:
        self._grafo: GrafoPonderadoDirecionado = grafo
        self._dist, self._prev, self._indice, self._vertices = _floyd_warshall(grafo)


    def travel_cost(self, origem: str, destino: str) -> Optional[float]:
        """
        Retorna o custo mínimo em minutos entre dois bairros

        Args:
            origem (str): Bairro de partida
            destino (str): Bairro de chegada

        Returns:
            Optional[float]: Custo em minutos, ou None se não houver caminho
        """

        i = self._indice.get(origem)
        j = self._indice.get(destino)

        if i is None or j is None:
            return None

        custo = self._dist[i][j]
        return None if custo == math.inf else custo


    def travel_path(self, origem: str, destino: str) -> Optional[list]:
        """
        Retorna a sequência de bairros do caminho mínimo entre dois pontos

        Args:
            origem (str): Bairro de partida
            destino (str): Bairro de chegada

        Returns:
            Optional[list]: Lista de bairros do caminho, ou None se não houver caminho
        """

        return _reconstruir_caminho(self._prev, self._indice, self._vertices, origem, destino)


    def _calcular_score(self, entrega: EntregaDia, t_atual: int, posicao: str) -> tuple:
        """
        Calcula o score de prioridade de uma entrega no instante atual

        Args:
            entrega (EntregaDia): Entrega candidata
            t_atual (int): Tempo corrente em minutos desde 09:00
            posicao (str): Bairro onde o entregador se encontra

        Returns:
            tuple: (score_numerico, nome_bairro, entrega) para comparação na heap
        """

        custo = self.travel_cost(posicao, entrega.bairro)

        if custo is None:
            return (math.inf, entrega.bairro, entrega)

        t_chegada = t_atual + custo
        penalidade = max(0, t_chegada - entrega.janela_fim)
        score = -(entrega.prioridade * 10) + custo + (penalidade * 2)
        return (score, entrega.bairro, entrega)


    def rotear(self, hub_inicial: str, entregas: list, hubs_finais: list) -> dict:
        """
        Executa a heurística gulosa e retorna o relatório completo da rota

        Args:
            hub_inicial (str): Bairro de partida do turno
            entregas (list): Lista de EntregaDia a serem realizadas
            hubs_finais (list): Lista de hubs candidatos para encerrar o turno

        Returns:
            dict: Relatório com rota, tempo total, log de decisões e entregas fora da janela
        """

        t = 0
        posicao = hub_inicial
        pendentes = [e for e in entregas]
        rota_bairros = [hub_inicial]
        log_decisoes = []

        while pendentes:
            heap = HeapMinima()

            for entrega in pendentes:
                custo = self.travel_cost(posicao, entrega.bairro)

                if custo is not None:
                    heap.inserir(self._calcular_score(entrega, t, posicao))

            if heap.vazia():
                break

            score_val, _, escolhida = heap.extrair_minimo()
            custo = self.travel_cost(posicao, escolhida.bairro)
            t_chegada = t + custo
            espera = max(0, escolhida.janela_inicio - t_chegada)
            t_saida = t_chegada + espera

            if t_chegada < escolhida.janela_inicio:
                status = "ANTES DA JANELA (esperou)"

            elif t_chegada <= escolhida.janela_fim:
                status = "NO PRAZO"
            
            else:
                status = "FORA DA JANELA"

            caminho_trecho = self.travel_path(posicao, escolhida.bairro)
            
            for bairro_intermediario in (caminho_trecho[1:] if caminho_trecho else []):
                if bairro_intermediario != escolhida.bairro:
                    rota_bairros.append(bairro_intermediario)
            
            rota_bairros.append(escolhida.bairro)
            log_decisoes.append({
                "bairro": escolhida.bairro,
                "score": round(score_val, 2),
                "t_partida": t,
                "custo_deslocamento": custo,
                "t_chegada": t_chegada,
                "espera": espera,
                "t_saida": t_saida,
                "janela": (escolhida.janela_inicio, escolhida.janela_fim),
                "status": status,
            })

            escolhida.concluida = True
            pendentes = [e for e in pendentes if not e.concluida]
            t = t_saida
            posicao = escolhida.bairro

        melhor_hub_final = None
        melhor_custo_retorno = math.inf

        for hub in hubs_finais:
            custo_hub = self.travel_cost(posicao, hub)

            if custo_hub is not None and custo_hub < melhor_custo_retorno:
                melhor_custo_retorno = custo_hub
                melhor_hub_final = hub

        if melhor_hub_final:
            caminho_retorno = self.travel_path(posicao, melhor_hub_final)
            
            for bairro_intermediario in (caminho_retorno[1:] if caminho_retorno else []):
                rota_bairros.append(bairro_intermediario)
            
            t += melhor_custo_retorno
        
        else:
            melhor_custo_retorno = None

        fora_da_janela = [d for d in log_decisoes if "FORA" in d["status"]]
        return {
            "hub_inicial": hub_inicial,
            "hub_final": melhor_hub_final,
            "rota": rota_bairros,
            "tempo_total": t,
            "custo_retorno": melhor_custo_retorno,
            "log": log_decisoes,
            "fora_da_janela": fora_da_janela,
        }


VERTICES = ["Centro", "Barra", "Botafogo", "Copacabana", "Ipanema", "Tijuca", "Madureira", "Jacarepagua",]
ARESTAS = [
    ("Centro", "Botafogo", 18),
    ("Centro", "Tijuca", 16),
    ("Centro", "Madureira", 34),
    ("Botafogo", "Copacabana", 10),
    ("Botafogo", "Ipanema", 14),
    ("Botafogo", "Centro", 20),
    ("Copacabana", "Ipanema", 9),
    ("Copacabana", "Botafogo", 12),
    ("Copacabana", "Centro", 28),
    ("Ipanema", "Copacabana", 10),
    ("Ipanema", "Botafogo", 16),
    ("Ipanema", "Barra", 30),
    ("Tijuca", "Centro", 18),
    ("Tijuca", "Madureira", 26),
    ("Tijuca", "Botafogo", 22),
    ("Madureira", "Tijuca", 30),
    ("Madureira", "Centro", 35),
    ("Madureira", "Jacarepagua", 28),
    ("Jacarepagua", "Barra", 18),
    ("Jacarepagua", "Madureira", 26),
    ("Barra", "Jacarepagua", 16),
    ("Barra", "Ipanema", 32),
    ("Barra", "Centro", 40),
]

ENTREGAS = [
    EntregaDia("Copacabana", 10, 45, 4),
    EntregaDia("Ipanema", 25, 75, 5),
    EntregaDia("Tijuca", 15, 60, 3),
    EntregaDia("Madureira", 60, 130, 3),
    EntregaDia("Jacarepagua", 80, 150, 2),
    EntregaDia("Botafogo", 20, 70, 2),
]

grafo = GrafoPonderadoDirecionado(VERTICES)

for origem, destino, peso in ARESTAS:
    grafo.adicionar_aresta(origem, destino, peso)

roteador = RoteadorEntregas(grafo)


print("\n===== Teste 1 - Estrutura do Grafo =====\n")

print(f"Representacao: {grafo}\n")

for bairro in ["Centro", "Madureira"]:
    vizinhos = grafo.vizinhos(bairro)
    print(f"Vizinhos de '{bairro}':")

    for destino, peso in vizinhos:
        print(f"  -> {destino}: {peso} min")

    print()


print("\n===== Teste 2 - Tabela de Menores Caminhos (Floyd-Warshall) =====\n")

pontos_relevantes = ["Centro", "Barra", "Botafogo", "Copacabana", "Ipanema", "Tijuca", "Madureira", "Jacarepagua"]
print(f"{'':>14}", end = "")

for v in pontos_relevantes:
    print(f"  {v[:5]:>5}", end = "")

print()
print("-" * (14 + 7 * len(pontos_relevantes)))

for origem in pontos_relevantes:
    print(f"{origem:<14}", end = "")

    for destino in pontos_relevantes:
        custo = roteador.travel_cost(origem, destino)

        if custo is None:
            print(f"  {'inf':>5}", end = "")
        
        else:
            print(f"  {custo:>5.0f}", end = "")
    
    print()


print("\n\n===== Teste 3 - Justificativa da Escolha do Hub Inicial =====\n")

print(f"{'Destino':<15}  {'Centro':>8}  {'Barra':>8}")
print(f"{'-' * 15}  {'-' * 8}  {'-' * 8}")

soma_centro = soma_barra = 0
bairros_entrega = [e.bairro for e in ENTREGAS]

for bairro in bairros_entrega:
    c_centro = roteador.travel_cost("Centro", bairro) or math.inf
    c_barra = roteador.travel_cost("Barra", bairro) or math.inf
    soma_centro += c_centro
    soma_barra += c_barra
    print(f"{bairro:<15}  {c_centro:>8.0f}  {c_barra:>8.0f}")

print(f"{'-' * 15}  {'-' * 8}  {'-' * 8}")
print(f"{'SOMA':<15}  {soma_centro:>8.0f}  {soma_barra:>8.0f}")
hub_escolhido = "Centro" if soma_centro <= soma_barra else "Barra"
print(f"\nHub escolhido: {hub_escolhido} (menor soma de custos para todos os bairros de entrega)")

print("\nEntregas mais urgentes (janela_inicio <= 25):")
urgentes = sorted(ENTREGAS, key=lambda e: e.janela_inicio)

for e in urgentes[:3]:
    c = roteador.travel_cost(hub_escolhido, e.bairro)
    folga = e.janela_fim - c if c else None
    print(f"  {e.bairro:<15} janela=[{e.janela_inicio:>3},{e.janela_fim:>4}] custo={c:>3} min folga={folga:>3} min")


print("\n\n===== Teste 4 - Log de Execução da Rota =====\n")

relatorio = roteador.rotear(hub_inicial=hub_escolhido, entregas=ENTREGAS, hubs_finais=["Centro", "Barra"])

print(f"{'#':<3}  {'Bairro':<15}  {'Score':>7}  {'t_part':>6}  {'custo':>5}  {'t_cheg':>6}  {'espera':>6}  {'t_said':>6}  {'Janela':<12}  Status")
print(f"{'-' * 3}  {'-' * 15}  {'-' * 7}  {'-' * 6}  {'-' * 5}  {'-' * 6}  {'-' * 6}  {'-' * 6}  {'-' * 12}  {'-' * 25}")

for i, d in enumerate(relatorio["log"], 1):
    janela_str = f"[{d['janela'][0]},{d['janela'][1]}]"
    print(
        f"{i:<3}  {d['bairro']:<15}  {d['score']:>7}  {d['t_partida']:>6}  "
        f"{d['custo_deslocamento']:>5}  {d['t_chegada']:>6}  {d['espera']:>6}  "
        f"{d['t_saida']:>6}  {janela_str:<12}  {d['status']}"
    )


print("\n\n===== Teste 5 - Relatório Final =====\n")

print(f"Hub inicial: {relatorio['hub_inicial']}")
print(f"Hub final: {relatorio['hub_final']}")
print(f"Custo retorno: {relatorio['custo_retorno']} min")
print(f"Tempo total: {relatorio['tempo_total']} min (encerra às {9*60 + relatorio['tempo_total']} min abs = {9 + relatorio['tempo_total']//60}h{relatorio['tempo_total']%60:02d})")
print(f"Entregas realizadas: {len(relatorio['log'])}")
print(f"Fora da janela: {len(relatorio['fora_da_janela'])}")
print()

print(f"Rota completa:")
print(f"  {' -> '.join(relatorio['rota'])}")
print()

if relatorio["fora_da_janela"]:
    print("Entregas fora da janela:")

    for d in relatorio["fora_da_janela"]:
        atraso = d["t_chegada"] - d["janela"][1]
        print(f"  {d['bairro']:<15} chegada t={d['t_chegada']} janela={d['janela']} atraso={atraso} min")

else:
    print("Todas as entregas foram realizadas dentro da janela.")


print("\n\n===== Teste 6 - Verificação de Caminhos Sem Rota =====\n")

pares_teste = [
    ("Gerona", "Madrid"),
    ("Tijuca", "Barra"),
    ("Barra", "Tijuca"),
    ("Copacabana", "Jacarepagua"),
]

for u, v in pares_teste:
    custo = roteador.travel_cost(u, v)

    if u not in VERTICES or v not in VERTICES:
        print(f"  {u} -> {v}: vértice inexistente, travel_cost retornou {custo} (sem quebra)")

    elif custo is None:
        print(f"  {u} -> {v}: sem caminho disponível, travel_cost retornou None (sem quebra)")

    else:
        caminho = roteador.travel_path(u, v)
        print(f"  {u} -> {v}: {custo} min | caminho: {' -> '.join(caminho)}")
print()
