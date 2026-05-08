from typing import Dict, List
import time


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


print("\n===== Teste 1 - Prefixo com mais palavras do que k =====\n")

trie6 = Trie()
palavras = ["car", "cart", "carro", "cartão", "caramelizar", "cartucho", "bola", "bolo", "boa"]

for p in palavras:
    trie6.insert(p)

resultado = trie6.autocomplete("car", 3)
print(f"=> autocomplete('car', 3): {resultado}")
print(f"Total de palavras com prefixo 'car': {len(trie6._collect_words(trie6.root.children['c'].children['a'].children['r'], 'car'))}\n")


print("\n===== Teste 2 - Prefixo com menos palavras do que k =====\n")

resultado = trie6.autocomplete("bo", 10)
print(f"=> autocomplete('bo', 10): {resultado}")
print(f"k=10, mas apenas {len(resultado)} palavra(s) encontrada(s) com prefixo 'bo'\n")


print("\n===== Teste 3 - Prefixo inexistente =====\n")

resultado = trie6.autocomplete("xyz", 5)
print(f"=> autocomplete('xyz', 5): {resultado}\n")


print("\n===== Teste 4 - Estabilidade da ordenação =====\n")

r1 = trie6.autocomplete("car", 5)
r2 = trie6.autocomplete("car", 5)
print(f"Primeira chamada: {r1}")
print(f"Segunda chamada: {r2}")
print(f"Resultados idênticos: {r1 == r2}\n")


print("\n===== Teste 5 - Custo no pior caso =====\n")

trie7 = Trie()
alfabeto = "abcdefghij"
inseridas = 0

for a in alfabeto:
    for b in alfabeto:
        for c in alfabeto:
            trie7.insert(a + b + c)
            inseridas += 1

inicio = time.perf_counter()
trie7.autocomplete("a", inseridas)
tempo = time.perf_counter() - inicio

print(f"Palavras inseridas: {inseridas}")
print(f"Prefixo 'a' cobre 1/{len(alfabeto)} da trie")
print(f"Tempo para autocomplete com k=total: {tempo * 1000:.3f} ms\n")
