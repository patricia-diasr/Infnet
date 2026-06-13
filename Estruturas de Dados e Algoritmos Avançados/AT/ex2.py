from typing import Optional


class BuscadorErroPrefixoNaoEncontrado(Exception):
    """Levantada quando nenhum termo com o prefixo informado existe na Trie"""


class ItemHeapSugestao:
    """
    Entrada interna da heap de sugestões que representa um termo candidato

    Attributes:
        peso (int): Peso do termo, usado como chave primária de comparação
        termo (str): Palavra candidata, usada como chave de desempate lexicográfico
    """

    def __init__(self, peso: int, termo: str) -> None:
        self.peso: int = peso
        self.termo: str = termo


    def __lt__(self, outro: "ItemHeapSugestao") -> bool:
        if self.peso != outro.peso:
            return self.peso < outro.peso

        return self.termo > outro.termo


    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ItemHeapSugestao):
            return NotImplemented

        return self.peso == outro.peso and self.termo == outro.termo


    def __repr__(self) -> str:
        return f"ItemHeapSugestao(peso = {self.peso}, termo = {self.termo!r})"


class HeapMinimaSugestoes:
    """
    Heap mínima de tamanho fixo K usada para rastrear os K termos de maior peso

    Attributes:
        _capacidade (int): Número máximo de elementos que a heap mantém simultaneamente
        _dados (list): Vetor interno dos itens válidos
        _tamanho (int): Número de itens válidos atualmente na heap
    """

    def __init__(self, capacidade: int) -> None:
        self._capacidade: int = capacidade
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
        """
        Restaura a propriedade de heap subindo o elemento na posição i

        Args:
            i (int): Índice do elemento a ser subido
        """

        while i > 0:
            pai = self._pai(i)

            if self._dados[i] < self._dados[pai]:
                self._trocar(i, pai)
                i = pai

            else:
                break


    def _descer(self, i: int) -> None:
        """
        Restaura a propriedade de heap descendo o elemento na posição i

        Args:
            i (int): Índice do elemento a ser descido
        """

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


    def _inserir_direto(self, item: ItemHeapSugestao) -> None:
        """
        Insere um item sem verificar a capacidade, usado internamente

        Args:
            item (ItemHeapSugestao): Item a ser inserido
        """

        if self._tamanho < len(self._dados):
            self._dados[self._tamanho] = item

        else:
            self._dados.append(item)

        self._tamanho += 1
        self._subir(self._tamanho - 1)


    def _extrair_minimo(self) -> ItemHeapSugestao:
        """
        Remove e retorna o item de menor prioridade da heap, ou seja, o pior dos K selecionados

        Returns:
            ItemHeapSugestao: Item com menor prioridade
        """

        self._trocar(0, self._tamanho - 1)
        self._tamanho -= 1
        item = self._dados[self._tamanho]

        if self._tamanho > 0:
            self._descer(0)

        return item


    def oferecer(self, peso: int, termo: str) -> None:
        """
        Oferece um candidato à heap, inserindo-o se ele for melhor que o pior atual

        Args:
            peso (int): Peso do termo candidato
            termo (str): Palavra candidata
        """

        candidato = ItemHeapSugestao(peso, termo)

        if self._tamanho < self._capacidade:
            self._inserir_direto(candidato)
            return

        topo = self._dados[0]
        candidato_melhor = (peso > topo.peso or (peso == topo.peso and termo < topo.termo))

        if candidato_melhor:
            self._extrair_minimo()
            self._inserir_direto(candidato)


    def extrair_todos_ordenados(self) -> list:
        """
        Remove e retorna todos os itens ordenados do maior para o menor peso

        Returns:
            list: Lista de tuplas (termo, peso) do maior para o menor peso
        """

        resultado = []

        while self._tamanho > 0:
            item = self._extrair_minimo()
            resultado.append((item.termo, item.peso))

        resultado.reverse()
        return resultado


    def tamanho(self) -> int:
        """
        Retorna o número de itens válidos na heap

        Returns:
            int: Quantidade de itens
        """

        return self._tamanho


    def __repr__(self) -> str:
        return f"HeapMinimaSugestoes(capacidade = {self._capacidade}, tamanho = {self._tamanho})"


class NodoTrie:
    """
    Nodo de uma Trie que representa um caractere no caminho de um termo

    Attributes:
        filhos (dict): Mapeamento de caractere para NodoTrie filho
        fim_de_termo (bool): Indica se este nodo encerra um termo válido
        peso (int): Peso do termo encerrado aqui, ou zero se não for fim de termo
    """

    def __init__(self) -> None:
        self.filhos: dict = {}
        self.fim_de_termo: bool = False
        self.peso: int = 0


    def __repr__(self) -> str:
        return (f"NodoTrie(filhos = {list(self.filhos.keys())}, fim_de_termo = {self.fim_de_termo}, peso = {self.peso})")


class BuscadorPrefixo:
    """
    Estrutura de busca por prefixo baseada em Trie com sugestão dos K termos mais relevantes

    Attributes:
        _raiz (NodoTrie): Nodo raiz da Trie, sem caractere associado
        _total_termos (int): Número de termos distintos armazenados
    """

    def __init__(self) -> None:
        self._raiz: NodoTrie = NodoTrie()
        self._total_termos: int = 0


    def inserir_termo(self, termo: str, peso: int) -> None:
        """
        Insere um termo e seu peso na Trie, atualizando o peso se o termo já existir

        Args:
            termo (str): Palavra a ser inserida
            peso (int): Relevância ou frequência de busca do termo
        """

        nodo = self._raiz

        for caractere in termo:
            if caractere not in nodo.filhos:
                nodo.filhos[caractere] = NodoTrie()

            nodo = nodo.filhos[caractere]

        if nodo.fim_de_termo:
            if peso > nodo.peso:
                nodo.peso = peso

        else:
            nodo.fim_de_termo = True
            nodo.peso = peso
            self._total_termos += 1


    def _localizar_prefixo(self, prefixo: str) -> Optional[NodoTrie]:
        """
        Navega pela Trie até o nodo correspondente ao último caractere do prefixo

        Args:
            prefixo (str): Prefixo a ser localizado

        Returns:
            Optional[NodoTrie]: Nodo do último caractere do prefixo, ou None se inexistente
        """

        nodo = self._raiz

        for caractere in prefixo:
            if caractere not in nodo.filhos:
                return None

            nodo = nodo.filhos[caractere]

        return nodo


    def _dfs_coletar(self, nodo: NodoTrie, prefixo_acumulado: str, heap: HeapMinimaSugestoes) -> None:
        """
        Percorre em profundidade a subárvore a partir de nodo, oferecendo termos à heap

        Args:
            nodo (NodoTrie): Nodo atual do percurso
            prefixo_acumulado (str): Termo construído até o nodo atual
            heap (HeapMinimaSugestoes): Heap que mantém os K melhores candidatos
        """

        if nodo.fim_de_termo:
            heap.oferecer(nodo.peso, prefixo_acumulado)

        for caractere, filho in nodo.filhos.items():
            self._dfs_coletar(filho, prefixo_acumulado + caractere, heap)


    def sugerir_top_k(self, prefixo: str, k: int) -> list:
        """
        Retorna até K termos que começam com o prefixo, ordenados por peso decrescente

        Args:
            prefixo (str): Prefixo digitado pelo usuário
            k (int): Número máximo de sugestões a retornar

        Returns:
            list: Lista de tuplas (termo, peso) com até K elementos

        Raises:
            BuscadorErroPrefixoNaoEncontrado: Se nenhum termo com o prefixo existir
        """

        nodo_prefixo = self._localizar_prefixo(prefixo)

        if nodo_prefixo is None:
            raise BuscadorErroPrefixoNaoEncontrado(f"Nenhum termo encontrado com o prefixo '{prefixo}'")

        heap = HeapMinimaSugestoes(k)
        self._dfs_coletar(nodo_prefixo, prefixo, heap)

        if heap.tamanho() == 0:
            raise BuscadorErroPrefixoNaoEncontrado(f"Nenhum termo encontrado com o prefixo '{prefixo}'")

        return heap.extrair_todos_ordenados()


    def total_termos(self) -> int:
        """
        Retorna o número de termos distintos armazenados na Trie

        Returns:
            int: Quantidade de termos
        """

        return self._total_termos


    def __repr__(self) -> str:
        return f"BuscadorPrefixo(total_termos = {self._total_termos})"


banco_de_palavras = [
    ("teclado", 45),
    ("tecnologia", 90),
    ("tecnico", 75),
    ("tecido", 30),
    ("computacao", 100),
    ("computador", 100),
    ("compilador", 85),
    ("complexo", 85),
    ("componente", 60),
    ("compartilhar", 95),
    ("comunidade", 70),
    ("comunismo", 10),
    ("copo", 40),
    ("carro", 55),
]

buscador = BuscadorPrefixo()

for termo, peso in banco_de_palavras:
    buscador.inserir_termo(termo, peso)


print("\n===== Teste 1 - Estado Inicial =====\n")
print(f"Termos inseridos: {buscador.total_termos()}")
print(f"Representacao: {buscador}")


print("\n\n===== Teste 2 - Sugestões por Prefixo =====\n")

consultas = [
    ("tec", 3),
    ("com", 5),
    ("comp", 4),
    ("comu", 3),
    ("computad", 2),
    ("c", 5),
]

for prefixo, k in consultas:
    resultado = buscador.sugerir_top_k(prefixo, k)
    print(f"Prefixo '{prefixo}' | Top {k}:")

    for i, (termo, peso) in enumerate(resultado, 1):
        print(f"  {i}. {termo:<20} (peso {peso})")

    print()


print("\n===== Teste 3 - Empate de Peso com Desempate Lexicográfico =====\n")

resultado_comp = buscador.sugerir_top_k("comp", 4)
print("Prefixo 'comp' | Top 4 (empates esperados em peso 100 e 85):")

for i, (termo, peso) in enumerate(resultado_comp, 1):
    print(f"  {i}. {termo:<20} (peso {peso})")

pesos = [p for _, p in resultado_comp]
termos_peso_100 = [t for t, p in resultado_comp if p == 100]
termos_peso_85 = [t for t, p in resultado_comp if p == 85]

print(f"\nPesos em ordem decrescente: {pesos == sorted(pesos, reverse=True)}")
print(f"Termos com peso 100 em ordem lexicografica: {termos_peso_100}")
print(f"Termos com peso 85 em ordem lexicografica: {termos_peso_85}")


print("\n\n===== Teste 4 - Atualização de Peso =====\n")

buscador.inserir_termo("teclado", 200)
resultado_tec = buscador.sugerir_top_k("tec", 4)
print("Prefixo 'tec' após atualizar 'teclado' para peso 200:")

for i, (termo, peso) in enumerate(resultado_tec, 1):
    print(f"  {i}. {termo:<20} (peso {peso})")

print(f"\nTotal de termos sem duplicata: {buscador.total_termos()}")

buscador.inserir_termo("teclado", 1)
resultado_tec2 = buscador.sugerir_top_k("tec", 4)
print("\nPrefixo 'tec' após tentar atualizar 'teclado' para peso menor (1):")

for i, (termo, peso) in enumerate(resultado_tec2, 1):
    print(f"  {i}. {termo:<20} (peso {peso})")

peso_teclado = next(p for t, p in resultado_tec2 if t == "teclado")
print(f"\nPeso de 'teclado' mantido em: {peso_teclado} (esperado: 200)")


print("\n\n===== Teste 5 - Prefixo Inexistente =====\n")

try:
    buscador.sugerir_top_k("xyz", 3)

except BuscadorErroPrefixoNaoEncontrado as e:
    print(f"Exceção esperada: {e}")


print("\n\n===== Teste 6 - K Maior que o Total de Termos Disponíveis =====\n")

resultado_comu = buscador.sugerir_top_k("comu", 10)
print("Prefixo 'comu' com k=10 (apenas 2 termos existem):")
for i, (termo, peso) in enumerate(resultado_comu, 1):
    
    print(f"  {i}. {termo:<20} (peso {peso})")

print(f"Quantidade retornada: {len(resultado_comu)} (esperado: 2)\n")
