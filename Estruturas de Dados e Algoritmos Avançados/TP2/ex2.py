from typing import Dict


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


print("\n===== Teste 1 - Busca de palavra existente =====\n")

trie3 = Trie()
trie3.insert("car")
trie3.insert("cart")
trie3.insert("carro")

print(f"=> search('car'): {trie3.search('car')}")
print(f"=> search('cart'): {trie3.search('cart')}")
print(f"=> search('carro'): {trie3.search('carro')}\n")


print("\n===== Teste 2 - Busca de palavra inexistente com prefixo existente =====\n")

print(f"=> search('carta'): {trie3.search('carta')} (prefixo 'cart' existe, mas 'carta' não)")
print(f"=> search('carros'): {trie3.search('carros')} (prefixo 'carro' existe, mas 'carros' não)\n")


print("\n===== Teste 3 - Busca de prefixo que não é palavra completa =====\n")

print(f"=> search('ca'): {trie3.search('ca')} (caminho existe, mas is_end=False no nó 'a')")
print(f"=> search('c'): {trie3.search('c')} (caminho existe, mas is_end=False no nó 'c')\n")


print("\n===== Teste 4 - Busca de palavra vazia =====\n")

print(f"=> search(''): {trie3.search('')}")
print("Decisão: palavra vazia retorna False pois root.is_end é False por padrão e nenhuma inserção marca a raiz como fim de palavra\n")
