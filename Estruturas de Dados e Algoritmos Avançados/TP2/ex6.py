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


print("\n===== Teste 1 - Palavra correta existente =====\n")

trie8 = Trie()
vocabulario = ["car", "cart", "carro", "carta", "cartão", "bola", "bolo", "boa", "barco"]

for p in vocabulario:
    trie8.insert(p)

print(f"=> autocorrect('car'): {trie8.autocorrect('car')}")
print(f"=> autocorrect('bola'): {trie8.autocorrect('bola')}\n")


print("\n===== Teste 2 - Palavra com erro no final =====\n")

print(f"=> autocorrect('cartt'): {trie8.autocorrect('cartt')}")
print("'cartt' compartilha 'cart' com 'cart' e 'cartão', retorna a menor lexicograficamente\n")


print("\n===== Teste 3 - Palavra com erro no meio =====\n")

print(f"=> autocorrect('caxro'): {trie8.autocorrect('caxro')}")
print("'caxro' diverge em 'x' após 'ca', subárvore de 'ca' cobre car/cart/carro/carta/cartão\n")


print("\n===== Teste 4 - Prefixo comum pequeno =====\n")

print(f"=> autocorrect('barca'): {trie8.autocorrect('barca')}")
print("'barca' compartilha apenas 'bar' com 'barco'\n")


print("\n===== Teste 5 - Palavra totalmente fora do vocabulário =====\n")

print(f"=> autocorrect('xyz'): {trie8.autocorrect('xyz')}")
print("'xyz' não compartilha nenhum prefixo, candidatas coletadas a partir da raiz")
print(f"Menor palavra da trie lexicograficamente: {sorted(vocabulario)[0]}\n")


print("\n===== Teste 6 - Empate de prefixo máximo =====\n")

print(f"=> autocorrect('carx'): {trie8.autocorrect('carx')}")
print("'carx' diverge após 'car', candidatas: car/cart/carro/carta/cartão")
print(f"Candidatas ordenadas: {sorted(trie8._collect_words(trie8.root.children['c'].children['a'].children['r'], 'car'))}")
print("Critério de desempate: menor lexicograficamente -> 'car'\n")
