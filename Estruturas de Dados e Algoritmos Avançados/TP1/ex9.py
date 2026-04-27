from typing import List, Tuple
import random
import time

class HeapUnderflowError(Exception):
    """Levantada ao tentar remover de uma BinaryHeap vazia"""


class HeapValueError(Exception):
    """Levantada ao tentar remover um valor inexistente da BinaryHeap"""


class BinaryHeap:
    """
    Heap Binária Máxima baseada em array

    Attributes:
        _dados (List[int]): Array interno de armazenamento, sem pré-alocação fixa
        trocas (List[Tuple[int, int, int, int]]): Registro de cada troca realizada durante operações de reorganização, no formato (indice_a, valor_a, indice_b, valor_b)
    """

    def __init__(self) -> None:
        self._dados: List[int] = []
        self.trocas: List[Tuple[int, int, int, int]] = []
        

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

        while i > 0:
            pai = self.indice_pai(i)

            if self._dados[i] > self._dados[pai]:
                self.trocas.append((i, self._dados[i], pai, self._dados[pai]))
                self._dados[i], self._dados[pai] = self._dados[pai], self._dados[i]
                i = pai

            else:
                break


    def _sift_down(self, i: int) -> None:
        """
        Reorganiza o heap de cima para baixo a partir do índice i, restaurando a invariante após uma remoção

        Args:
            i (int): Índice inicial para a descida
        """

        n = len(self._dados)

        while True:
            maior = i
            esq = self.indice_filho_esquerdo(i)
            dir = self.indice_filho_direito(i)

            if esq < n and self._dados[esq] > self._dados[maior]:
                maior = esq

            if dir < n and self._dados[dir] > self._dados[maior]:
                maior = dir

            if maior != i:
                self.trocas.append((i, self._dados[i], maior, self._dados[maior]))
                self._dados[i], self._dados[maior] = self._dados[maior], self._dados[i]
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

        self._dados.append(valor)
        self._sift_up(len(self._dados) - 1)


    def extract_max(self) -> int:
        """
        Remove e retorna o elemento de maior valor da heap

        Returns:
            int: O maior valor presente na heap antes da remoção

        Raises:
            HeapUnderflowError: Se a heap estiver vazia
        """

        if not self._dados:
            raise HeapUnderflowError("Heap underflow: heap vazia")

        maximo = self._dados[0]
        ultimo = self._dados.pop()

        if self._dados:
            self._dados[0] = ultimo
            self._sift_down(0)

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

        self._dados = list(array)
        self.trocas.clear()

        n = len(self._dados)
        ultimo_interno = (n // 2) - 1

        for i in range(ultimo_interno, -1, -1):
            self._sift_down(i)


    def esta_vazia(self) -> bool:
        return len(self._dados) == 0
    

    def __len__(self) -> int:
        return len(self._dados)


    def __repr__(self) -> str:
        return f"BinaryHeap(raiz={self._dados[0] if self._dados else None}, dados={self._dados})"


def comparar_construcao(array: List[int]) -> Tuple[int, int, float, float]:
    """
    Compara a construção de uma heap pelos métodos inserção incremental (insert) e construção direta (build_heap)

    Args:
        array (List[int]): Array de entrada a ser transformado em heap

    Returns:
        Tuple[int, int, float, float]: Tupla com (trocas_insert, trocas_build, tempo_insert, tempo_build)
    """

    heap_insert = BinaryHeap()
    inicio = time.perf_counter()
    
    for v in array:
        heap_insert.insert(v)
    
    tempo_insert = time.perf_counter() - inicio
    trocas_insert = len(heap_insert.trocas)
    heap_build = BinaryHeap()
    inicio = time.perf_counter()
    heap_build.build_heap(array)
    tempo_build = time.perf_counter() - inicio
    trocas_build = len(heap_build.trocas)

    return trocas_insert, trocas_build, tempo_insert, tempo_build


print("\n===== Teste 1 - Comparação por Número de Trocas (tamanhos variados) =====\n")

random.seed(42)
tamanhos = [10, 50, 100, 500, 1000]

print(f"{'N':>6}  {'Trocas insert':>14}  {'Trocas build':>13}  {'Redução':>8}")
print(f"{'-'*6}  {'-'*14}  {'-'*13}  {'-'*8}")

for n in tamanhos:
    array = random.sample(range(1, n * 10), n)
    trocas_insert, trocas_build, _, _ = comparar_construcao(array)
    reducao = trocas_insert - trocas_build
    print(f"{n:>6}  {trocas_insert:>14}  {trocas_build:>13}  {reducao:>+8}")


print("\n\n===== Teste 2 - Comparação por Ordem de Entrada =====\n")

n = 100
arrays = {
    "aleatório": random.sample(range(1, 1000), n),
    "crescente": list(range(1, n + 1)),
    "decrescente": list(range(n, 0, -1)),
}

print(f"{'Ordem':>12}  {'Trocas insert':>14}  {'Trocas build':>13}  {'Redução':>8}")
print(f"{'-'*12}  {'-'*14}  {'-'*13}  {'-'*8}")

for ordem, array in arrays.items():
    trocas_insert, trocas_build, _, _ = comparar_construcao(array)
    reducao = trocas_insert - trocas_build
    print(f"{ordem:>12}  {trocas_insert:>14}  {trocas_build:>13}  {reducao:>+8}")


print("\n\n===== Teste 3 - Comparação de Tempo de Execução =====\n")

random.seed(42)
array_grande = random.sample(range(1, 100_000), 10_000)
trocas_insert, trocas_build, tempo_insert, tempo_build = comparar_construcao(array_grande)

print(f"N = {len(array_grande)} elementos")
print(f"Inserção incremental -> {trocas_insert} trocas em {tempo_insert * 1000:.3f} ms")
print(f"Build_heap -> {trocas_build} trocas em {tempo_build * 1000:.3f} ms")
print(f"Trocas economizadas: {trocas_insert - trocas_build}")
print(f"Speedup aproximado: {tempo_insert / tempo_build:.2f}x\n")
