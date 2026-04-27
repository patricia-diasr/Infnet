from typing import List, Tuple
import random
import time
import math


class HeapUnderflowError(Exception):
    """Levantada ao tentar remover de uma BinaryHeap vazia"""


class HeapValueError(Exception):
    """Levantada ao tentar remover um valor inexistente da BinaryHeap"""


class MetricasHeap:
    """
    Registro acumulado de operações primitivas executadas pela BinaryHeap

    Attributes:
        comparacoes (int): Total de comparações entre elementos realizadas
        trocas (int): Total de trocas de posição entre elementos realizadas
        acessos (int): Total de leituras individuais no array interno
        chamadas_sift_up (int): Número de invocações de _sift_up
        chamadas_sift_down (int): Número de invocações de _sift_down
        chamadas_insert (int): Número de invocações de insert
        chamadas_extract_max (int): Número de invocações de extract_max
        chamadas_build_heap (int): Número de invocações de build_heap
        tempo_total_segundos (float): Tempo acumulado de execução em segundos
    """

    def __init__(self) -> None:
        self.comparacoes: int = 0
        self.trocas: int = 0
        self.acessos: int = 0
        self.chamadas_sift_up: int = 0
        self.chamadas_sift_down: int = 0
        self.chamadas_insert: int = 0
        self.chamadas_extract_max: int = 0
        self.chamadas_build_heap: int = 0
        self.tempo_total_segundos: float = 0.0

    def zerar(self) -> None:
        """Reinicia todos os contadores para zero"""
        self.comparacoes = 0
        self.trocas = 0
        self.acessos = 0
        self.chamadas_sift_up = 0
        self.chamadas_sift_down = 0
        self.chamadas_insert = 0
        self.chamadas_extract_max = 0
        self.chamadas_build_heap = 0
        self.tempo_total_segundos = 0.0

    def __repr__(self) -> str:
        return (f"MetricasHeap(comparacoes={self.comparacoes}, trocas={self.trocas}, acessos={self.acessos}, tempo={self.tempo_total_segundos * 1000:.4f}ms)")


class BinaryHeap:
    """
    Heap Binária Máxima baseada em array

    Attributes:
        _dados (List[int]): Array interno de armazenamento, sem pré-alocação fixa
        trocas (List[Tuple[int, int, int, int]]): Registro de cada troca realizada durante operações de reorganização, no formato (indice_a, valor_a, indice_b, valor_b)
        metricas (MetricasHeap): Contadores de operações primitivas para análise empírica de complexidade
    """

    def __init__(self) -> None:
        self._dados: List[int] = []
        self.trocas: List[Tuple[int, int, int, int]] = []
        self.metricas: MetricasHeap = MetricasHeap()
        

    def indice_pai(self, i: int) -> int:
        """
        Retorna o índice do pai do nó i

        Args:
            i (int): Índice do nó filho

        Returns:
            int: Índice do nó pai
        """

        return (i - 1) // 2


    def indice_filho_esquerdo(self, i: int) -> int:
        """
        Retorna o índice do filho esquerdo do nó i

        Args:
            i (int): Índice do nó pai

        Returns:
            int: Índice do filho esquerdo
        """

        return 2 * i + 1


    def indice_filho_direito(self, i: int) -> int:
        """
        Retorna o índice do filho direito do nó i

        Args:
            i (int): Índice do nó pai

        Returns:
            int: Índice do filho direito
        """

        return 2 * i + 2


    def _sift_up(self, i: int) -> None:
        """
        Reorganiza o heap de baixo para cima a partir do índice i, restaurando a invariante após uma inserção

        Args:
            i (int): Índice inicial para a subida
        """

        self.metricas.chamadas_sift_up += 1

        while i > 0:
            pai = self.indice_pai(i)
            self.metricas.acessos += 2
            self.metricas.comparacoes += 1

            if self._dados[i] > self._dados[pai]:
                self.trocas.append((i, self._dados[i], pai, self._dados[pai]))
                self._dados[i], self._dados[pai] = self._dados[pai], self._dados[i]
                self.metricas.trocas += 1
                i = pai

            else:
                break


    def _sift_down(self, i: int) -> None:
        """
        Reorganiza o heap de cima para baixo a partir do índice i, restaurando a invariante após uma remoção

        Args:
            i (int): Índice inicial para a descida
        """

        self.metricas.chamadas_sift_down += 1
        n = len(self._dados)

        while True:
            maior = i
            esq = self.indice_filho_esquerdo(i)
            dir = self.indice_filho_direito(i)
            self.metricas.acessos += 2

            if esq < n and self._dados[esq] > self._dados[maior]:
                self.metricas.comparacoes += 1
                maior = esq

            if dir < n and self._dados[dir] > self._dados[maior]:
                self.metricas.comparacoes += 1
                maior = dir

            if maior != i:
                self.trocas.append((i, self._dados[i], maior, self._dados[maior]))
                self._dados[i], self._dados[maior] = self._dados[maior], self._dados[i]
                self.metricas.trocas += 1
                i = maior

            else:
                break


    def _buscar_indice(self, valor: int) -> int:
        """
        Localiza o índice de um valor no array interno via busca linear

        Args:
            valor (int): Valor a ser localizado

        Returns:
            int: Índice do valor no array interno

        Raises:
            HeapValueError: Se o valor não estiver presente na heap
        """

        for i, elemento in enumerate(self._dados):
            if elemento == valor:
                return i

        raise HeapValueError(f"Valor {valor} não encontrado na heap")
    

    def insert(self, valor: int) -> None:
        """
        Insere um valor na heap preservando todas as invariantes

        Args:
            valor (int): Valor inteiro a ser inserido
        """

        inicio = time.perf_counter()
        self.metricas.chamadas_insert += 1
        self._dados.append(valor)
        self._sift_up(len(self._dados) - 1)
        self.metricas.tempo_total_segundos += time.perf_counter() - inicio


    def extract_max(self) -> int:
        """
        Remove e retorna o elemento de maior valor da heap

        Returns:
            int: O maior valor presente na heap antes da remoção

        Raises:
            HeapUnderflowError: Se a heap estiver vazia
        """

        inicio = time.perf_counter()

        if not self._dados:
            raise HeapUnderflowError("Heap underflow: heap vazia")

        self.metricas.chamadas_extract_max += 1
        maximo = self._dados[0]
        ultimo = self._dados.pop()

        if self._dados:
            self._dados[0] = ultimo
            self._sift_down(0)

        self.metricas.tempo_total_segundos += time.perf_counter() - inicio
        return maximo
    

    def contains(self, valor: int) -> bool:
        """
        Verifica se um valor está presente na heap via busca linear

        Args:
            valor (int): Valor a ser buscado

        Returns:
            bool: True se o valor estiver presente, False caso contrário
        """

        for elemento in self._dados:
            if elemento == valor:
                return True

        return False
    

    def delete(self, valor: int) -> None:
        """
        Remove um elemento arbitrário da heap preservando todas as invariantes

        Args:
            valor (int): Valor a ser removido

        Raises:
            HeapUnderflowError: Se a heap estiver vazia
            HeapValueError: Se o valor não estiver presente na heap
        """

        if not self._dados:
            raise HeapUnderflowError("Heap underflow: heap vazia")

        indice_alvo = self._buscar_indice(valor)
        ultimo = self._dados.pop()

        if indice_alvo < len(self._dados):
            self._dados[indice_alvo] = ultimo
            self._sift_up(indice_alvo)
            self._sift_down(indice_alvo)


    def build_heap(self, array: List[int]) -> None:
        """
        Constrói a heap a partir de um array arbitrário sem inserções individuais

        Args:
            array (List[int]): Array de inteiros a ser transformado em heap
        """

        inicio = time.perf_counter()
        self.metricas.chamadas_build_heap += 1
        self._dados = list(array)
        self.trocas.clear()
        n = len(self._dados)
        ultimo_interno = (n // 2) - 1

        for i in range(ultimo_interno, -1, -1):
            self._sift_down(i)

        self.metricas.tempo_total_segundos += time.perf_counter() - inicio


    def esta_vazia(self) -> bool:
        return len(self._dados) == 0
    

    def __len__(self) -> int:
        return len(self._dados)


    def __repr__(self) -> str:
        return f"BinaryHeap(raiz={self._dados[0] if self._dados else None}, dados={self._dados})"


def coletar_metricas_insert(tamanho: int, semente: int = 0) -> MetricasHeap:
    """
    Constrói uma heap de tamanho n por inserções individuais e retorna as métricas acumuladas da operação completa

    Args:
        tamanho (int): Número de elementos a inserir
        semente (int): Semente para geração do array aleatório

    Returns:
        MetricasHeap: Métricas coletadas após todas as inserções
    """

    random.seed(semente)
    array = random.sample(range(1, tamanho * 10 + 1), tamanho)
    heap = BinaryHeap()

    for v in array:
        heap.insert(v)

    return heap.metricas


def coletar_metricas_build(tamanho: int, semente: int = 0) -> MetricasHeap:
    """
    Constrói uma heap de tamanho n via build_heap e retorna as métricas acumuladas da operação completa

    Args:
        tamanho (int): Número de elementos no array de entrada
        semente (int): Semente para geração do array aleatório

    Returns:
        MetricasHeap: Métricas coletadas após a construção
    """

    random.seed(semente)
    array = random.sample(range(1, tamanho * 10 + 1), tamanho)
    heap = BinaryHeap()
    heap.build_heap(array)
    return heap.metricas


def coletar_metricas_extract(tamanho: int, semente: int = 0) -> MetricasHeap:
    """
    Constrói uma heap de tamanho n e realiza n extrações sucessivas, retornando as métricas acumuladas apenas das extrações

    Args:
        tamanho (int): Número de elementos e de extrações a realizar
        semente (int): Semente para geração do array aleatório

    Returns:
        MetricasHeap: Métricas coletadas após todas as extrações
    """

    random.seed(semente)
    array = random.sample(range(1, tamanho * 10 + 1), tamanho)
    heap = BinaryHeap()
    heap.build_heap(array)
    heap.metricas.zerar()

    while not heap.esta_vazia():
        heap.extract_max()

    return heap.metricas


def referencia_teorica_insert(n: int) -> float:
    """
    Calcula o valor de referência teórico para n inserções individuais

    Args:
        n (int): Número de elementos

    Returns:
        float: n * log2(n)
    """

    return n * math.log2(n) if n > 1 else 0.0


def referencia_teorica_build(n: int) -> float:
    """
    Calcula o valor de referência teórico para build_heap

    Args:
        n (int): Número de elementos

    Returns:
        float: n
    """

    return float(n)


def referencia_teorica_extract(n: int) -> float:
    """
    Calcula o valor de referência teórico para n extrações sucessivas

    Args:
        n (int): Número de extrações

    Returns:
        float: n * log2(n)
    """

    return n * math.log2(n) if n > 1 else 0.0


tamanhos = [50, 100, 250, 500, 1000, 2500, 5000]
semente = 42

print("\n===== Teste 1 - Comparações Empíricas: Inserções Individuais =====\n")
print(f"{'N':>6}  {'Comparacoes':>12}  {'Trocas':>7}  {'n*log2(n)':>10}  {'Razão comp/teorico':>19}  {'Tempo (ms)':>10}")
print(f"{'-'*6}  {'-'*12}  {'-'*7}  {'-'*10}  {'-'*19}  {'-'*10}")

for n in tamanhos:
    m = coletar_metricas_insert(n, semente)
    teorico = referencia_teorica_insert(n)
    razao = m.comparacoes / teorico if teorico > 0 else 0.0
    print(f"{n:>6}  {m.comparacoes:>12}  {m.trocas:>7}  {teorico:>10.1f}  {razao:>19.4f}  {m.tempo_total_segundos * 1000:>10.4f}")


print("\n\n===== Teste 2 - Comparações Empíricas: build_heap (Floyd) =====\n")
print(f"{'N':>6}  {'Comparacoes':>12}  {'Trocas':>7}  {'N (ref)':>10}  {'Razão comp/teorico':>19}  {'Tempo (ms)':>10}")
print(f"{'-'*6}  {'-'*12}  {'-'*7}  {'-'*10}  {'-'*19}  {'-'*10}")

for n in tamanhos:
    m = coletar_metricas_build(n, semente)
    teorico = referencia_teorica_build(n)
    razao = m.comparacoes / teorico if teorico > 0 else 0.0
    print(f"{n:>6}  {m.comparacoes:>12}  {m.trocas:>7}  {teorico:>10.1f}  {razao:>19.4f}  {m.tempo_total_segundos * 1000:>10.4f}")


print("\n\n===== Teste 3 - Comparações Empíricas: Extrações Sucessivas =====\n")
print(f"{'N':>6}  {'Comparacoes':>12}  {'Trocas':>7}  {'n*log2(n)':>10}  {'Razão comp/teorico':>19}  {'Tempo (ms)':>10}")
print(f"{'-'*6}  {'-'*12}  {'-'*7}  {'-'*10}  {'-'*19}  {'-'*10}")

for n in tamanhos:
    m = coletar_metricas_extract(n, semente)
    teorico = referencia_teorica_extract(n)
    razao = m.comparacoes / teorico if teorico > 0 else 0.0
    print(f"{n:>6}  {m.comparacoes:>12}  {m.trocas:>7}  {teorico:>10.1f}  {razao:>19.4f}  {m.tempo_total_segundos * 1000:>10.4f}")


print("\n\n===== Teste 4 - Crescimento Relativo: Insert vs Build_heap =====\n")
print(f"{'N':>6}  {'Comp insert':>12}  {'Comp build':>11}  {'Razão insert/build':>19}")
print(f"{'-'*6}  {'-'*12}  {'-'*11}  {'-'*19}")

for n in tamanhos:
    m_insert = coletar_metricas_insert(n, semente)
    m_build  = coletar_metricas_build(n, semente)
    razao = m_insert.comparacoes / m_build.comparacoes if m_build.comparacoes > 0 else 0.0
    print(f"{n:>6}  {m_insert.comparacoes:>12}  {m_build.comparacoes:>11}  {razao:>19.4f}")


print("\n\n===== Teste 5 - Estabilidade da Razão empírico/teórico por Ordem de Entrada =====\n")

n_fixo = 1000

ordens: List[Tuple[str, List[int]]] = [
    ("aleatória", random.sample(range(1, 10_001), n_fixo)),
    ("crescente", list(range(1, n_fixo + 1))),
    ("decrescente", list(range(n_fixo, 0, -1))),
]

print(f"N = {n_fixo}\n")
print(f"{'Ordem':>12}  {'Comp insert':>12}  {'Comp build':>11}  {'Razão i/b':>10}")
print(f"{'-'*12}  {'-'*12}  {'-'*11}  {'-'*10}")

for nome, array in ordens:
    heap_i = BinaryHeap()
    for v in array:
        heap_i.insert(v)

    heap_b = BinaryHeap()
    heap_b.build_heap(array)

    razao = (
        heap_i.metricas.comparacoes / heap_b.metricas.comparacoes
        if heap_b.metricas.comparacoes > 0
        else 0.0
    )

    print(f"{nome:>12}  {heap_i.metricas.comparacoes:>12}  {heap_b.metricas.comparacoes:>11}  {razao:>10.4f}")
print()
