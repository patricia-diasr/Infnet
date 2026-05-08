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


print("\n===== Teste 1 - Traversal completo a partir da raiz =====\n")

trie5 = Trie()
palavras_originais = ["car", "cart", "carro", "cartão", "bola", "bolo", "boa"]

for p in palavras_originais:
    trie5.insert(p)

palavras_coletadas = trie5._collect_words(trie5.root, "")

print(f"Palavras inseridas: {sorted(palavras_originais)}")
print(f"Palavras coletadas: {sorted(palavras_coletadas)}\n")


print("\n===== Teste 2 - Traversal a partir de um prefixo específico =====\n")

prefixo = "car"
no_prefixo = trie5.root

for char in prefixo:
    no_prefixo = no_prefixo.children[char]

palavras_do_prefixo = trie5._collect_words(no_prefixo, prefixo)

print(f"Prefixo usado: '{prefixo}'")
print(f"Palavras encontradas: {sorted(palavras_do_prefixo)}\n")


print("\n===== Teste 3 - Verificação de perdas e duplicações =====\n")

originais = set(palavras_originais)
coletadas = set(palavras_coletadas)

perdidas = originais - coletadas
duplicadas = [p for p in palavras_coletadas if palavras_coletadas.count(p) > 1]

print(f"Total inserido: {len(palavras_originais)}")
print(f"Total coletado: {len(palavras_coletadas)}")
print(f"Palavras perdidas: {perdidas if perdidas else 'nenhuma'}")
print(f"Palavras duplicadas: {duplicadas if duplicadas else 'nenhuma'}")
print(f"Conjuntos idênticos: {originais == coletadas}\n")
