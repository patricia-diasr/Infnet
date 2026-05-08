import sys
import time
import random
import string
from typing import Dict, List


class TrieNode:
    """
    Nó individual de uma Trie

    Attributes:
        children (Dict[str, TrieNode]): Mapeamento de caracteres para nós filhos
        is_end (bool): Indica se este nó representa o fim de uma palavra
    """

    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """
    Trie (árvore de prefixos) para armazenamento e busca de palavras

    Attributes:
        root (TrieNode): Nó raiz da Trie, sem caractere associado
    """

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()


    def insert(self, word: str) -> None:
        """
        Insere uma palavra na Trie caractere a caractere

        Args:
            word (str): Palavra a ser inserida
        """

        atual = self.root

        for char in word:
            if char not in atual.children:
                atual.children[char] = TrieNode()

            atual = atual.children[char]

        atual.is_end = True


    def search(self, word: str) -> bool:
        """
        Verifica se uma palavra completa está presente na Trie

        Args:
            word (str): Palavra a ser buscada

        Returns:
            bool: True se a palavra existir como entrada completa, False caso contrário
        """

        atual = self.root

        for char in word:
            if char not in atual.children:
                return False

            atual = atual.children[char]

        return atual.is_end


    def starts_with(self, prefix: str) -> bool:
            """
            Verifica se existe alguma palavra na Trie com o prefixo informado

            Args:
                prefix (str): Prefixo a ser buscado

            Returns:
                bool: True se o prefixo existir como caminho na Trie, False caso contrário
            """

            atual = self.root

            for char in prefix:
                if char not in atual.children:
                    return False
                
                atual = atual.children[char]

            return True

    
    def autocomplete(self, prefix: str, k: int) -> List[str]:
        """
        Retorna até k sugestões de palavras que começam com o prefixo informado, ordenadas lexicograficamente

        Args:
            prefix (str): Prefixo a ser usado como ponto de partida
            k (int): Número máximo de sugestões a retornar

        Returns:
            List[str]: Lista com até k palavras ordenadas lexicograficamente
        """

        atual = self.root

        for char in prefix:
            if char not in atual.children:
                return []

            atual = atual.children[char]

        return sorted(self._collect_words(atual, prefix))[:k]


    def _collect_words(self, node: TrieNode, prefix: str) -> List[str]:
        """
        Coleta recursivamente todas as palavras na subárvore a partir de um nó

        Args:
            node (TrieNode): Nó raiz da subárvore a percorrer
            prefix (str): Prefixo acumulado até o nó atual

        Returns:
            List[str]: Lista de todas as palavras encontradas na subárvore
        """

        resultado: List[str] = []

        if node.is_end:
            resultado.append(prefix)

        for char, filho in node.children.items():
            resultado.extend(self._collect_words(filho, prefix + char))

        return resultado


    def autocorrect(self, word: str) -> str | None:
        """
        Retorna a palavra mais próxima na Trie com base no maior prefixo compartilhado

        Args:
            word (str): Palavra a ser corrigida

        Returns:
            str | None: Palavra corrigida, ou None se a Trie estiver vazia
        """

        if self.search(word):
            return word

        atual = self.root
        maior_prefixo = ""

        for char in word:
            if char not in atual.children:
                break

            atual = atual.children[char]
            maior_prefixo += char

        candidatas = self._collect_words(atual, maior_prefixo)

        if not candidatas:
            return None

        return sorted(candidatas)[0]


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


print("\n===== Teste 1 - Custo das operações da Trie em função do comprimento da palavra =====\n")

trie_perf = Trie()
palavras_base = [
    "a", "ab", "abc", "abcd", "abcde",
    "abcdef", "abcdefg", "abcdefgh", "abcdefghi", "abcdefghij",
]

for p in palavras_base:
    trie_perf.insert(p)

repeticoes = 200_000
resultados = []

for p in palavras_base:
    inicio = time.perf_counter()

    for _ in range(repeticoes):
        trie_perf.insert(p)

    t_insert = (time.perf_counter() - inicio) * 1000
    inicio = time.perf_counter()

    for _ in range(repeticoes):
        trie_perf.search(p)

    t_search = (time.perf_counter() - inicio) * 1000
    inicio = time.perf_counter()

    for _ in range(repeticoes):
        trie_perf.starts_with(p)

    t_starts = (time.perf_counter() - inicio) * 1000
    resultados.append((len(p), t_insert, t_search, t_starts))

print(f"{'|p|':>4}  {'insert (ms)':>11}  {'search (ms)':>11}  {'starts_with (ms)':>16}")
print(f"{'-'*4}  {'-'*11}  {'-'*11}  {'-'*16}")

for comp, ti, ts, tsw in resultados:
    print(f"{comp:>4}  {ti:>11.3f}  {ts:>11.3f}  {tsw:>16.3f}")

print(f"\n(médias sobre {repeticoes} repetições por palavra)\n")


print("\n===== Teste 2 - Custo do autocomplete em função do tamanho da subárvore =====\n")

trie_auto = Trie()
random.seed(42)
alfabeto = "abcdefghij"
todas = []

for a in alfabeto:
    for b in alfabeto:
        for c in alfabeto:
            todas.append(a + b + c)

for p in todas:
    trie_auto.insert(p)

prefixos_teste = ["a", "ab", "abc"]
repeticoes_auto = 1_000

print(f"{'prefixo':>8}  {'subárvore':>10}  {'autocomplete k=10 (ms)':>22}  {'autocomplete k=all (ms)':>23}")
print(f"{'-'*8}  {'-'*10}  {'-'*22}  {'-'*23}")

for pref in prefixos_teste:
    sub = len(trie_auto.autocomplete(pref, len(todas)))
    inicio = time.perf_counter()

    for _ in range(repeticoes_auto):
        trie_auto.autocomplete(pref, 10)
    
    t_k10 = (time.perf_counter() - inicio) * 1000
    inicio = time.perf_counter()

    for _ in range(repeticoes_auto):
        trie_auto.autocomplete(pref, sub)
    
    t_all = (time.perf_counter() - inicio) * 1000
    print(f"{pref:>8}  {sub:>10}  {t_k10:>22.3f}  {t_all:>23.3f}")

print(f"\n(médias sobre {repeticoes_auto} repetições por prefixo)\n")


print("\n===== Teste 3 - Custo de has_edge: lista vs matriz em grafos esparsos e densos =====\n")

def build_sparse(n: int) -> tuple:
    gl = GraphAdjList()
    gm = GraphAdjMatrix()
    arestas = []

    for i in range(n):
        gl.add_vertex(i)
        gm.add_vertex(i)

    for i in range(n - 1):
        gl.add_edge(i, i + 1)
        gm.add_edge(i, i + 1)
        arestas.append((i, i + 1))

    return gl, gm, arestas


def build_dense(n: int) -> tuple:
    gl = GraphAdjList()
    gm = GraphAdjMatrix()
    arestas = []

    for i in range(n):
        gl.add_vertex(i)
        gm.add_vertex(i)

    for i in range(n):
        for j in range(i + 1, n):
            gl.add_edge(i, j)
            gm.add_edge(i, j)
            arestas.append((i, j))

    return gl, gm, arestas


repeticoes_edge = 50_000
configs = [("esparso", 50), ("denso", 20)]

print(f"{'config':>10}  {'n':>4}  {'arestas':>8}  {'t_lista (ms)':>13}  {'t_matriz (ms)':>13}")
print(f"{'-'*10}  {'-'*4}  {'-'*8}  {'-'*13}  {'-'*13}")

for nome, n in configs:
    gl, gm, arestas = (build_sparse(n) if nome == "esparso" else build_dense(n))
    u, v = arestas[len(arestas) // 2]
    inicio = time.perf_counter()

    for _ in range(repeticoes_edge):
        _ = v in gl.adj[u]
    
    t_lista = (time.perf_counter() - inicio) * 1000
    inicio = time.perf_counter()

    for _ in range(repeticoes_edge):
        gm.has_edge(u, v)
    
    t_matriz = (time.perf_counter() - inicio) * 1000
    print(f"{nome:>10}  {n:>4}  {len(arestas):>8}  {t_lista:>13.3f}  {t_matriz:>13.3f}")

print(f"\n(médias sobre {repeticoes_edge} repetições)\n")


print("\n===== Teste 4 - Consumo de memória: lista vs matriz em função de n =====\n")

tamanhos = [10, 50, 100, 200]

print(f"{'n':>5}  {'arestas':>8}  {'mem_lista (bytes)':>18}  {'mem_matriz (bytes)':>19}  {'razão':>6}")
print(f"{'-'*5}  {'-'*8}  {'-'*18}  {'-'*19}  {'-'*6}")

for n in tamanhos:
    gl, gm, arestas = build_dense(n)
    mem_lista = sys.getsizeof(gl.adj) + sum(sys.getsizeof(s) for s in gl.adj.values())
    mem_matriz = (
        sys.getsizeof(gm.mat)
        + sum(sys.getsizeof(linha) for linha in gm.mat)
        + sys.getsizeof(gm.index)
    )

    razao = mem_matriz / mem_lista if mem_lista > 0 else 0
    print(f"{n:>5}  {len(arestas):>8}  {mem_lista:>18}  {mem_matriz:>19}  {razao:>6.2f}x")


print("\n\n===== Teste 5 - Decisão técnica: children como dict vs lista fixa =====\n")

trie_dict = Trie()

for word in ["abacate", "abacaxi", "abadia", "zebra", "zero"]:
    trie_dict.insert(word)

nos_raiz = len(trie_dict.root.children)
total_nos = sum(1 for _ in trie_dict._collect_words(trie_dict.root, ""))

print(f"Filhos diretos da raiz (dict): {list(trie_dict.root.children.keys())}")
print(f"Apenas {nos_raiz} de 26 entradas alocadas na raiz")
print(f"Com lista fixa de tamanho 26, cada nó alocaria 26 entradas independente do uso")
print(f"Com dict, nós folha com is_end=True alocam 0 entradas em children\n")


print("\n===== Teste 6 - Decisão técnica: set vs list nos vizinhos do GraphAdjList =====\n")

g_set = GraphAdjList()
g_set.add_edge(0, 1)
g_set.add_edge(0, 1)
g_set.add_edge(0, 1)

print(f"Após 3 inserções da aresta (0,1) com set: adj[0] = {g_set.adj[0]}")
print(f"Sem duplicatas: {len(g_set.adj[0]) == 1}")
print(f"has_edge via 'v in set': O(1) médio, vs O(grau) com list\n")
