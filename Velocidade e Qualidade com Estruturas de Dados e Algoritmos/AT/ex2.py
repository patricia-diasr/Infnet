from typing import List, Optional, Tuple
import random
import time


def bubble_sort(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista utilizando o algoritmo Bubble Sort

    Args:
        arr (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[List[int], int, int]:
            - lista ordenada (cópia)
            - número de comparações realizadas
            - número de cópias realizadas (troca = 3 cópias)
    """

    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    copias = 0

    for i in range(n - 1):
        houve_troca = False
    
        for j in range(n - 1 - i):
            comparacoes += 1
    
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                copias += 3
                houve_troca = True
    
        if not houve_troca:
            break

    return lista, comparacoes, copias


def selection_sort(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista utilizando o algoritmo Selection Sort

    Args:
        arr (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[List[int], int, int]:
            - lista ordenada (cópia)
            - número de comparações realizadas
            - número de cópias realizadas (troca = 3 cópias)
    """

    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    copias = 0

    for i in range(n - 1):
        indice_minimo = i

        for j in range(i + 1, n):
            comparacoes += 1
        
            if lista[j] < lista[indice_minimo]:
                indice_minimo = j
        
        if indice_minimo != i:
            lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]
            copias += 3

    return lista, comparacoes, copias


def insertion_sort(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista utilizando o algoritmo Insertion Sort.

    Args:
        arr (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[List[int], int, int]:
            - lista ordenada (cópia)
            - número de comparações realizadas
            - número de cópias realizadas (deslocamento = 1 cópia por posição)
    """

    lista = arr.copy()
    n = len(lista)
    comparacoes = 0
    copias = 0

    for i in range(1, n):
        chave = lista[i]
        copias += 1
        j = i - 1

        while j >= 0:
            comparacoes += 1
            
            if lista[j] > chave:
                lista[j + 1] = lista[j]
                copias += 1
                j -= 1
            
            else:
                break
        
        lista[j + 1] = chave
        copias += 1

    return lista, comparacoes, copias


def gerar_quase_ordenado(n: int, perturbacoes: int = None) -> List[int]:
    """
    Gera um vetor quase ordenado trocando um número reduzido de pares de posições aleatórias em uma lista originalmente ordenada

    Args:
        n (int): Tamanho do vetor
        perturbacoes (int): Número de trocas aleatórias. Padrão: max(1, n // 20)

    Returns:
        List[int]: Lista quase ordenada com n elementos
    """
    
    if perturbacoes is None:
        perturbacoes = max(1, n // 20)

    lista = list(range(1, n + 1))

    for _ in range(perturbacoes):
        i, j = random.sample(range(n), 2)
        lista[i], lista[j] = lista[j], lista[i]
    
    return lista


def gerar_padroes(n: int) -> dict:
    """
    Gera os quatro padrões de entrada para um dado tamanho n

    Args:
        n (int): Número de elementos em cada padrão

    Returns:
        dict: Chaves 'ordenado', 'reverso', 'quase_ordenado', 'aleatorio', cada uma mapeando para um List[int] de tamanho n
    """

    base = list(range(1, n + 1))
    aleatorio = base.copy()
    random.shuffle(aleatorio)
    
    return {
        "ordenado": base,
        "reverso": base[::-1],
        "quase_ordenado": gerar_quase_ordenado(n),
        "aleatorio": aleatorio,
    }


class NoBST:
    """
    Nó interno de uma Árvore Binária de Busca

    Attributes:
        valor (int): Chave armazenada no nó
        esquerda (Optional[NoBST]): Subárvore esquerda (valores menores)
        direita (Optional[NoBST]): Subárvore direita (valores maiores)
    """

    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.esquerda: Optional["NoBST"] = None
        self.direita: Optional["NoBST"] = None


class BinarySearchTree:
    """
    Árvore Binária de Busca de inteiros

    Attributes:
        raiz (Optional[NoBST]): Raiz da árvore
        comparacoes_insercao (int): Total de comparações em todas as inserções
        chamadas_inorder (int): Total de chamadas recursivas na travessia in-order
    """

    def __init__(self) -> None:
        self.raiz: Optional[NoBST] = None
        self.comparacoes_insercao: int = 0
        self.chamadas_inorder: int = 0

    def inserir(self, valor: int) -> None:
        """
        Insere um valor na posição correta da BST

        Args:
            valor (int): Inteiro a ser inserido
        """

        novo = NoBST(valor)

        if self.raiz is None:
            self.raiz = novo
            return

        atual = self.raiz

        while True:
            self.comparacoes_insercao += 1

            if valor < atual.valor:
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return
                atual = atual.esquerda

            elif valor > atual.valor:
                if atual.direita is None:
                    atual.direita = novo
                    return
                atual = atual.direita

            else:
                return

    def inorder(self) -> List[int]:
        """
        Realiza a travessia in-order (esquerda -> raiz -> direita), produzindo os elementos em ordem crescente

        Returns:
            List[int]: Elementos ordenados
        """

        resultado: List[int] = []
        pilha = []
        atual = self.raiz

        while atual is not None or pilha:
            while atual is not None:
                pilha.append(atual)
                atual = atual.esquerda

            atual = pilha.pop()
            self.chamadas_inorder += 1
            resultado.append(atual.valor)
            atual = atual.direita

        return resultado

    @classmethod
    def de_lista(cls, arr: List[int]) -> "BinarySearchTree":
        """
        Constrói uma BST inserindo todos os elementos de um array

        Args:
            arr (List[int]): Lista de inteiros de origem

        Returns:
            BinarySearchTree: Árvore populada com todos os elementos
        """

        arvore = cls()
        
        for valor in arr:
            arvore.inserir(valor)
        
        return arvore


def bst_sort(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Ordena uma lista construindo uma BST e executando a travessia in-order

    Args:
        arr (List[int]): Lista de inteiros a ser ordenada

    Returns:
        Tuple[List[int], int, int]:
            - lista ordenada
            - número de comparações realizadas nas inserções
            - número de chamadas à função de travessia in-order
    """

    arvore = BinarySearchTree.de_lista(arr)
    ordenado = arvore.inorder()
    return ordenado, arvore.comparacoes_insercao, arvore.chamadas_inorder


ALGORITMOS = {
    "bubble_sort": bubble_sort,
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "bst_sort": bst_sort,
}


def executar_experimento(tamanhos: List[int]) -> List[dict]:
    """
    Executa todos os algoritmos em todos os padrões para cada tamanho, registrando comparações, cópias e tempo de execução

    Args:
        tamanhos (List[int]): Sequência de tamanhos crescentes a testar

    Returns:
        List[dict]: Cada entrada representa uma combinação (algoritmo × padrão × tamanho) com suas métricas
    """

    resultados = []

    for n in tamanhos:
        padroes = gerar_padroes(n)

        for nome_padrao, vetor in padroes.items():
            for nome_algo, funcao in ALGORITMOS.items():
                inicio = time.perf_counter()
                _, comparacoes, copias = funcao(vetor)
                tempo = time.perf_counter() - inicio

                resultados.append({
                    "n": n,
                    "padrao": nome_padrao,
                    "algoritmo": nome_algo,
                    "comparacoes": comparacoes,
                    "copias": copias,
                    "tempo_s": tempo,
                })

    return resultados


random.seed(42)


print("\n===== Teste 1 - Validação dos algoritmos =====\n")

arr_teste = [64, 25, 12, 22, 11]
print(f"Array original: {arr_teste}\n")

for nome, funcao in ALGORITMOS.items():
    ordenado, comp, cop = funcao(arr_teste)
    print(f"{nome:<16} -> resultado={ordenado}, comparações={comp}, cópias={cop}")


print("\n\n===== Teste 2 - Experimento com padrões e escalas =====\n")

tamanhos = [1000, 10000, 25000]
resultados = executar_experimento(tamanhos)

padroes_ordem = ["ordenado", "quase_ordenado", "aleatorio", "reverso"]

for padrao in padroes_ordem:
    print(f"=> Padrão: {padrao}")
    print(f"{'algoritmo':<16}  {'n':>6}  {'comparações':>14}  {'cópias':>10}  {'tempo (s)':>10}")
    print("-" * 62)
    
    for r in resultados:
        if r["padrao"] == padrao:
            print(
                f"{r['algoritmo']:<16}  {r['n']:>6}  "
                f"{r['comparacoes']:>14}  {r['copias']:>10}  {r['tempo_s']:>10.5f}"
            )
    print()


print("\n===== Análise - Benefício do padrão quase ordenado =====\n")

n_analise = 25000
algoritmos_ordem = list(ALGORITMOS.keys())
print(f"Comparando comparações no padrão 'quase_ordenado' vs 'aleatorio' (n={n_analise}):\n")
print(f"=> {'algoritmo':<16}  {'quase_ord':>12}  {'aleatorio':>12}  {'redução %':>10}")
print("-" * 56)

for algo in algoritmos_ordem:
    comp_quase = next(
        r["comparacoes"] for r in resultados
        if r["algoritmo"] == algo and r["padrao"] == "quase_ordenado" and r["n"] == n_analise
    )
    comp_aleat = next(
        r["comparacoes"] for r in resultados
        if r["algoritmo"] == algo and r["padrao"] == "aleatorio" and r["n"] == n_analise
    )
    reducao = (1 - comp_quase / comp_aleat) * 100
    print(f"  {algo:<16}  {comp_quase:>12}  {comp_aleat:>12}  {reducao:>9.1f}%")
    