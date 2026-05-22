from typing import Dict, List, Optional, Tuple


class TrieNode:
    """
    Nó individual de uma Trie

    Attributes:
        filhos (Dict[str, TrieNode]): Mapeamento de caractéres para nós filhos
        fim_de_palavra (bool): Indica se este nó representa o fim de uma palavra
    """

    def __init__(self) -> None:
        self.filhos: Dict[str, "TrieNode"] = {}
        self.fim_de_palavra: bool = False


    def __repr__(self) -> str:
        return f"TrieNode(filhos = {list(self.filhos.keys())}, fim_de_palavra = {self.fim_de_palavra})"


class Trie:
    """
    Árvore de prefixos para armazenamento, busca e manipulação de palavras

    Attributes:
        _raiz (TrieNode): Nó raiz da Trie, sem caractere associado
        _tamanho (int): Número de palavras armazenadas na Trie
    """

    def __init__(self) -> None:
        self._raiz: TrieNode = TrieNode()
        self._tamanho: int = 0


    def inserir(self, palavra: str) -> None:
        """
        Insere uma palavra na Trie caractere a caractere

        Args:
            palavra (str): Palavra a ser inserida
        """

        atual = self._raiz

        for char in palavra.lower():
            if char not in atual.filhos:
                atual.filhos[char] = TrieNode()

            atual = atual.filhos[char]

        if not atual.fim_de_palavra:
            atual.fim_de_palavra = True
            self._tamanho += 1


    def buscar(self, palavra: str) -> bool:
        """
        Verifica se uma palavra completa está presente na Trie

        Args:
            palavra (str): Palavra a ser buscada

        Returns:
            bool: True se a palavra existir como entrada completa
        """

        no = self._buscar_no(palavra.lower())
        return no is not None and no.fim_de_palavra


    def tem_prefixo(self, prefixo: str) -> bool:
        """
        Verifica se existe alguma palavra na Trie com o prefixo informado

        Args:
            prefixo (str): Prefixo a ser verificado

        Returns:
            bool: True se o prefixo existir como caminho na Trie
        """

        return self._buscar_no(prefixo.lower()) is not None


    def remover(self, palavra: str) -> bool:
        """
        Remove uma palavra da Trie preservando prefixos compartilhados com outras palavras

        Args:
            palavra (str): Palavra a ser removida

        Returns:
            bool: True se a palavra existia e foi removida, False se não foi encontrada
        """

        encontrou, _ = self._remover_recursivo(self._raiz, palavra.lower(), 0)

        if encontrou:
            self._tamanho -= 1

        return encontrou


    def listar(self) -> List[str]:
        """
        Retorna todas as palavras armazenadas na Trie em ordem alfabética

        Returns:
            List[str]: Lista ordenada de todas as palavras
        """

        return sorted(self._coletar_palavras(self._raiz, ""))


    def autocompletar(self, prefixo: str, k: int = 10) -> List[str]:
        """
        Retorna até k sugestões de palavras que começam com o prefixo informado, em ordem alfabética

        Args:
            prefixo (str): Prefixo usado como ponto de partida
            k (int): Número máximo de sugestões a retornar

        Returns:
            List[str]: Lista com até k palavras ordenadas alfabéticamente
        """

        prefixo = prefixo.lower()
        no = self._buscar_no(prefixo)

        if no is None:
            return []

        return sorted(self._coletar_palavras(no, prefixo))[:k]


    def autocorrigir(self, palavra: str, max_distancia: int = 2) -> Optional[str]:
        """
        Retorna a palavra mais próxima na Trie usando distância de edição de Levenshtein

        Args:
            palavra (str): Palavra digitada possivelmente com erro
            max_distancia (int): Distância máxima de edição aceita para uma correção

        Returns:
            Optional[str]: Palavra mais próxima encontrada dentro da distância máxima, ou None se nenhuma candidata for viável
        """

        if self.buscar(palavra):
            return palavra

        palavra = palavra.lower()
        linha_atual = list(range(len(palavra) + 1))
        candidatas: List[Tuple[int, str]] = []
        self._busca_levenshtein(no=self._raiz, char_no="", palavra_alvo=palavra, prefixo_atual="", linha_anterior=linha_atual, max_distancia=max_distancia, candidatas=candidatas)

        if not candidatas:
            return None

        candidatas.sort(key=lambda t: (t[0], t[1]))
        return candidatas[0][1]


    def tamanho(self) -> int:
        """
        Retorna o número de palavras armazenadas na Trie

        Returns:
            int: Quantidade de palavras
        """

        return self._tamanho


    def para_mermaid(self) -> str:
        """
        Gera uma representação Mermaid da Trie.

        Returns:
            str: Código Mermaid da Trie
        """

        linhas = ["flowchart TD"]
        contador = 0

        def escapar(texto: str) -> str:
            return texto.replace('"', '\\"')

        def dfs(no: TrieNode, nome_no: str, prefixo: str) -> None:
            nonlocal contador
            label = "ROOT" if prefixo == "" else prefixo[-1]

            if no.fim_de_palavra:
                linhas.append(f'    {nome_no}["{escapar(label)} ✓"]')

            else:
                linhas.append(f'    {nome_no}["{escapar(label)}"]')

            for char, filho in sorted(no.filhos.items()):
                contador += 1
                filho_nome = f"n{contador}"
                linhas.append(f"    {nome_no} --> {filho_nome}")

                dfs(no=filho, nome_no=filho_nome, prefixo=prefixo + char)

        dfs(self._raiz, "root", "")
        return "\n".join(linhas)


    def _remover_recursivo(self, no: TrieNode, palavra: str, profundidade: int) -> Tuple[bool, bool]:
        """
        Percorre a Trie recursivamente e remove o marcador de fim de palavra, podando nós orfaos

        Args:
            no (TrieNode): Nó atual do percurso
            palavra (str): Palavra sendo removida
            profundidade (int): Índice do caractere atual na palavra

        Returns:
            Tuple[bool, bool]: (palavra_encontrada, no_pode_ser_podado)
        """

        if profundidade == len(palavra):
            if not no.fim_de_palavra:
                return False, False

            no.fim_de_palavra = False
            pode_podar = len(no.filhos) == 0
            return True, pode_podar

        char = palavra[profundidade]

        if char not in no.filhos:
            return False, False

        encontrou, pode_podar_filho = self._remover_recursivo(no.filhos[char], palavra, profundidade + 1)

        if pode_podar_filho:
            del no.filhos[char]

        pode_podar = not no.fim_de_palavra and len(no.filhos) == 0
        return encontrou, pode_podar


    def _busca_levenshtein(self, no: TrieNode, char_no: str, palavra_alvo: str, prefixo_atual: str, linha_anterior: List[int], max_distancia: int, candidatas: List[Tuple[int, str]]) -> None:
        """
        Percorre a Trie recursivamente calculando a distância de Levenshtein coluna a coluna

        Args:
            no (TrieNode): Nó atual do percurso na Trie
            char_no (str): Caractere associado ao nó atual
            palavra_alvo (str): Palavra que se deseja corrigir
            prefixo_atual (str): Palavra formada até o nó atual
            linha_anterior (List[int]): Linha anterior da matriz de Levenshtein
            max_distancia (int): Distância máxima tolerada para considerar uma candidata
            candidatas (List[Tuple[int, str]]): Lista acumuladora de pares (distancia, palavra)
        """

        colunas = len(palavra_alvo) + 1
        linha_atual = [linha_anterior[0] + 1]

        for coluna in range(1, colunas):
            custo_insercao = linha_atual[coluna - 1] + 1
            custo_remocao = linha_anterior[coluna] + 1
            custo_substituicao = linha_anterior[coluna - 1] + (0 if palavra_alvo[coluna - 1] == char_no else 1)
            linha_atual.append(min(custo_insercao, custo_remocao, custo_substituicao))

        if no.fim_de_palavra and linha_atual[-1] <= max_distancia:
            candidatas.append((linha_atual[-1], prefixo_atual))

        if min(linha_atual) <= max_distancia:
            for char, filho in no.filhos.items():
                self._busca_levenshtein(no=filho, char_no=char, palavra_alvo=palavra_alvo, prefixo_atual=prefixo_atual + char, linha_anterior=linha_atual, max_distancia=max_distancia, candidatas=candidatas)


    def _buscar_no(self, texto: str) -> Optional[TrieNode]:
        """
        Navega pela Trie seguindo os caracteres do texto e retorna o nó final

        Args:
            texto (str): Sequência de caracteres a ser seguida

        Returns:
            Optional[TrieNode]: Nó correspondente ao último caractere, ou None se o caminho não existir
        """

        atual = self._raiz

        for char in texto:
            if char not in atual.filhos:
                return None

            atual = atual.filhos[char]

        return atual


    def _coletar_palavras(self, no: TrieNode, prefixo: str) -> List[str]:
        """
        Coleta recursivamente todas as palavras na subárvore a partir de um nó

        Args:
            no (TrieNode): Nó raiz da subárvore a percorrer
            prefixo (str): Prefixo acumulado até o nó atual

        Returns:
            List[str]: Lista de todas as palavras encontradas na subárvore
        """

        resultado: List[str] = []

        if no.fim_de_palavra:
            resultado.append(prefixo)

        for char, filho in no.filhos.items():
            resultado.extend(self._coletar_palavras(filho, prefixo + char))

        return resultado


    def __repr__(self) -> str:
        return f"Trie(tamanho = {self._tamanho})"


palavras = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para",
    "com", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos",
    "como", "mas", "ao", "ele", "das", "seu", "sua", "ou", "quando", "muito",
    "nos", "ja", "eu", "tambem", "so", "pelo", "pela", "ate", "isso", "ela",
    "entre", "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse",
    "eles", "voce", "essa", "num", "nem", "suas", "meu", "as", "minha", "numa",
    "pelos", "elas", "qual", "nos", "lhe", "deles", "essas", "esses", "pelas", "este",
    "dele", "tu", "te", "voces", "vos", "lhes", "meus", "minhas", "teu", "tua",
    "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes",
    "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "esta", "estamos",
    "estao", "estava", "estar", "fui", "foi", "fomos", "foram", "sou", "somos", "sao",
    "tempo", "casa", "vida", "pessoa", "ano", "dia", "forma", "parte",
    "lugar", "vez", "mundo", "trabalho", "problema", "historia", "ponto",
    "empresa", "governo", "cidade", "pais", "estado",
]

trie = Trie()

for palavra in palavras:
    trie.inserir(palavra)


print("\n===== Teste 1 - Estado Inicial =====\n")
print(f"Palavras inseridas: {trie.tamanho()}")
print(f"Representação: {trie}\n")
print("Mermaid:")
print(trie.para_mermaid())


print("\n===== Teste 2 - Busca de Palavras =====\n")
buscas = ["de", "casa", "tempo", "python", "governo", "XYZ", "nossos", "aquilo"]

for palavra in buscas:
    encontrou = trie.buscar(palavra)
    status = "encontrada" if encontrou else "não encontrada"
    print(f"'{palavra}': {status}")


print("\n\n===== Teste 3 - Verificação de Prefixo =====\n")
prefixos = ["ca", "temp", "gov", "xyz", "no", "aqu"]

for prefixo in prefixos:
    tem = trie.tem_prefixo(prefixo)
    status = "existe" if tem else "não existe"
    print(f"Prefixo '{prefixo}': {status}")


print("\n\n===== Teste 4 - Autocompletar =====\n")
testes_autocompletar = [("ca", 5), ("est", 8), ("no", 6), ("aqu", 10)]

for prefixo, k in testes_autocompletar:
    sugestoes = trie.autocompletar(prefixo, k)
    print(f"Prefixo '{prefixo}' (ate {k} sugestões): {sugestoes}")


print("\n\n===== Teste 5 - Autocorreção =====\n")
erros_digitacao = [
    ("caza", "casa", 2),
    ("tmpeo", "tempo", 3),
    ("goverrno", "governo", 2),
    ("hstoria", "historia", 2),
    ("pesoa", "pessoa", 2),
    ("mundi", "mundo", 2),
    ("trabaho", "trabalho", 2),
    ("ciadde", "cidade", 3),
    ("esstou", "estou", 2),
    ("nososs", "nossos", 3),
]

print(f"{'Digitado':<15} {'Esperado':<15} {'Dist.':<7} {'Corrigido':<15} {'Acerto'}")
print(f"{'-'*15} {'-'*15} {'-'*7} {'-'*15} {'-'*6}")

acertos = 0
for digitado, esperado, distancia in erros_digitacao:
    corrigido = trie.autocorrigir(digitado, max_distancia=distancia)
    acertou = corrigido == esperado

    if acertou:
        acertos += 1
        
    marcador = "OK" if acertou else "FALHOU"
    print(f"{digitado:<15} {esperado:<15} {distancia:<7} {str(corrigido):<15} {marcador}")

print(f"\nPrecisao: {acertos}/{len(erros_digitacao)} ({100*acertos//len(erros_digitacao)}%)")


print("\n\n===== Teste 6 - Remoção de Palavras =====\n")
remover = ["casa", "tempo", "mundo"]

for palavra in remover:
    removeu = trie.remover(palavra)
    status = "removida" if removeu else "não encontrada"
    print(f"'{palavra}': {status}")

print(f"\nPalavras após remoção: {trie.tamanho()}")

print()
for palavra in remover:
    encontrou = trie.buscar(palavra)
    status = "ainda presente" if encontrou else "ausente confirmado"
    print(f"Busca por '{palavra}' após remoção: {status}")

tentativa = trie.remover("inexistente")
print(f"\nTentativa de remover palavra inexistente: {'removida' if tentativa else 'não encontrada'}")


print("\n\n===== Teste 7 - Listagem Completa =====\n")
todas = trie.listar()
print(f"Total de palavras listadas: {len(todas)}")
print(f"\nPrimeiras 20 em ordem alfabética:")

for i, palavra in enumerate(todas[:20], 1):
    print(f"  {i:>2}. {palavra}")

print(f"\nÚltimas 10 em ordem alfabética:")
for i, palavra in enumerate(todas[-10:], len(todas) - 9):
    print(f"  {i:>2}. {palavra}")


print("\n\n===== Teste 8 - Autocorreção com Distância Ampliada =====\n")
erros_distantes = [
    ("cazinha", 3),
    ("govermno", 2),
    ("prazem", 2),
]

for digitado, distancia in erros_distantes:
    corrigido = trie.autocorrigir(digitado, max_distancia=distancia)
    print(f"'{digitado}' (distancia={distancia}) -> '{corrigido}'")


print(f"\n\n===== Teste 9 - Estado Final =====\n")
print(f"Tamanho final: {trie.tamanho()} palavras")
print(f"Representação: {trie}\n")
