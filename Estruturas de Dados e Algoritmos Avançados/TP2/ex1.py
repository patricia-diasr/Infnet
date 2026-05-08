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


print("\n===== Teste 1 - Inserção de palavra nova =====\n")

trie = Trie()
trie.insert("carro")
atual = trie.root

for char in "carro":
    atual = atual.children[char]

print(f"Palavra 'carro' inserida")
print(f"Caminho percorrido: c -> a -> r -> r -> o")
print(f"is_end no último nó: {atual.is_end}\n")


print("\n===== Teste 2 - Inserção repetida da mesma palavra =====\n")

trie.insert("carro")
print(f"Inserção repetida de 'carro' realizada")
print(f"Filhos da raiz após segunda inserção: {list(trie.root.children.keys())}\n")


print("\n===== Teste 3 - Inserção de palavra que é prefixo de outra =====\n")

trie2 = Trie()
trie2.insert("cart")
trie2.insert("car")
no_r = trie2.root.children["c"].children["a"].children["r"]
no_t = no_r.children["t"]

print(f"'cart' inserida, depois 'car' (prefixo de 'cart')")
print(f"is_end no nó 'r' (fim de 'car'): {no_r.is_end}")
print(f"is_end no nó 't' (fim de 'cart'): {no_t.is_end}")
print(f"Filhos do nó 'r': {list(no_r.children.keys())}\n")
