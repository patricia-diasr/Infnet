import sys
import time
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


def find_vertices_by_prefix(trie: Trie, grafo: GraphAdjList, prefix: str, k: int) -> List[str]:
    """
    Retorna até k vértices do grafo cujos nomes começam com o prefixo informado

    Args:
        trie (Trie): Índice textual com os nomes dos vértices
        grafo (GraphAdjList): Grafo onde os vértices serão confirmados
        prefix (str): Prefixo a ser buscado
        k (int): Número máximo de resultados

    Returns:
        List[str]: Lista com até k nomes de vértices que começam com prefix
    """

    candidatos = trie.autocomplete(prefix, k)
    return [c for c in candidatos if c in grafo.adj]


print("\n===== Teste 1 - Construção do índice e do grafo =====\n")

nomes = [
    "auth-service", "auth-gateway", "auth-token",
    "user-api", "user-profile", "user-session",
    "payment-core", "payment-retry",
    "notification-email", "notification-sms",
    "log-aggregator",
]

trie_idx = Trie()
g_servicos = GraphAdjList()

for nome in nomes:
    trie_idx.insert(nome)
    g_servicos.add_vertex(nome)

arestas_servicos = [
    ("auth-gateway", "auth-service"),
    ("auth-gateway", "auth-token"),
    ("auth-service", "user-api"),
    ("user-api", "user-profile"),
    ("user-api", "user-session"),
    ("user-session", "auth-token"),
    ("payment-core", "user-api"),
    ("payment-core", "payment-retry"),
    ("notification-email", "user-profile"),
    ("notification-sms", "user-profile"),
    ("log-aggregator", "auth-service"),
    ("log-aggregator", "payment-core"),
]

for u, v in arestas_servicos:
    g_servicos.add_edge(u, v)

print(f"Vértices no grafo: {len(g_servicos.adj)}")
print(f"Arestas no grafo: {len(arestas_servicos)}")
print(f"Palavras na Trie: {len(trie_idx._collect_words(trie_idx.root, ''))}\n")


print("\n===== Teste 2 - Consistência entre Trie e grafo =====\n")

palavras_trie = set(trie_idx._collect_words(trie_idx.root, ""))
vertices_grafo = set(g_servicos.adj.keys())
apenas_trie = palavras_trie - vertices_grafo
apenas_grafo = vertices_grafo - palavras_trie

print(f"Apenas na Trie (não no grafo): {apenas_trie if apenas_trie else 'nenhum'}")
print(f"Apenas no grafo (não na Trie): {apenas_grafo if apenas_grafo else 'nenhum'}")
print(f"Índice consistente: {palavras_trie == vertices_grafo}\n")


print("\n===== Teste 3 - Consulta por prefixo 'auth' =====\n")

resultado = find_vertices_by_prefix(trie_idx, g_servicos, "auth", 10)
print(f"Prefixo 'auth', k=10: {resultado}")

for v in resultado:
    print(f"=> {v} -> vizinhos: {sorted(g_servicos.adj[v])}")


print("\n\n===== Teste 4 - Consulta por prefixo 'user' com k limitado =====\n")

resultado = find_vertices_by_prefix(trie_idx, g_servicos, "user", 2)
total_user = len(trie_idx.autocomplete("user", 100))
print(f"Prefixo 'user', k=2: {resultado}")
print(f"Total de vértices com prefixo 'user': {total_user}")
print(f"Resultados limitados pelo k: {len(resultado) <= 2}\n")


print("\n===== Teste 5 - Consulta por prefixo inexistente =====\n")

resultado = find_vertices_by_prefix(trie_idx, g_servicos, "cache", 5)
print(f"Prefixo 'cache', k=5: {resultado if resultado else '[]'}")
print(f"Nenhum vértice encontrado: {len(resultado) == 0}\n")


print("\n===== Teste 6 - Consulta por prefixo 'notification' =====\n")

resultado = find_vertices_by_prefix(trie_idx, g_servicos, "notification", 10)
print(f"Prefixo 'notification', k=10: {resultado}")

for v in resultado:
    print(f"=> {v} -> vizinhos: {sorted(g_servicos.adj[v])}")
print()
