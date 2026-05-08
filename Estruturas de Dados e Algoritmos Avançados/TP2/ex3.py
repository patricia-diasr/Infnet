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


print("\n===== Teste 1 - Prefixo que existe =====\n")

trie4 = Trie()
trie4.insert("car")
trie4.insert("cart")
trie4.insert("carro")
trie4.insert("cartão")
trie4.insert("bola")

print(f"=> starts_with('ca'): {trie4.starts_with('ca')}")
print(f"=> starts_with('car'): {trie4.starts_with('car')}")
print(f"=> starts_with('bo'): {trie4.starts_with('bo')}\n")


print("\n===== Teste 2 - Prefixo que não existe =====\n")

print(f"=> starts_with('x'): {trie4.starts_with('x')}")
print(f"=> starts_with('caz'): {trie4.starts_with('caz')}\n")


print("\n===== Teste 3 - Prefixo que é uma palavra completa =====\n")

print(f"=> starts_with('car'): {trie4.starts_with('car')} (é prefixo e também palavra completa)")
print(f"=> search('car'): {trie4.search('car')} (confirmação: é palavra completa)\n")


print("\n===== Teste 4 - Tabela com 5 prefixos e seus resultados =====\n")

prefixos = ["c", "ca", "car", "cart", "xyz"]

print(f"{'Prefixo':<10}  {'starts_with':>12}  {'search':>8}")
print(f"{'-'*10}  {'-'*12}  {'-'*8}")

for p in prefixos:
    print(f"{p:<10}  {str(trie4.starts_with(p)):>12}  {str(trie4.search(p)):>8}")
print()
