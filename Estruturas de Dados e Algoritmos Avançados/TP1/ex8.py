from typing import List, Tuple


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


def is_valid_heap(array: List[int]) -> bool:
    """
    Verifica se um array representa uma heap binária máxima válida

    Args:
        array (List[int]): Array a ser validado

    Returns:
        bool: True se o array representar uma heap máxima válida,
              False caso contrário
    """

    n = len(array)

    for i in range(n // 2):
        esq = 2 * i + 1
        dir = 2 * i + 2

        if esq < n and array[i] < array[esq]:
            return False

        if dir < n and array[i] < array[dir]:
            return False

    return True


print("\n===== Teste 1 - Construção de Heap com build_heap =====\n")

casos_build = [
    [3, 1, 6, 5, 2, 4],
    [1, 2, 3, 4, 5, 6, 7],
    [7, 6, 5, 4, 3, 2, 1],
    [42],
    [10, 20, 15, 30, 40],
]

for array in casos_build:
    heap_build = BinaryHeap()
    heap_build.build_heap(array)
    valido = is_valid_heap(heap_build._dados)
    status = "válida" if valido else "INVÁLIDA"

    print(f"Entrada: {array}")
    print(f"Heap: {heap_build._dados}")
    print(f"Trocas: {len(heap_build.trocas)}")
    print(f"Validação estrutural: {status}")
    print()


print("\n===== Teste 2 - Comparação: build_heap vs inserções individuais =====\n")

import random
random.seed(42)

array_grande = random.sample(range(1, 200), 15)
print(f"Array de entrada ({len(array_grande)} elementos): {array_grande}\n")

heap_build = BinaryHeap()
heap_build.build_heap(array_grande)
trocas_build = len(heap_build.trocas)

heap_insert = BinaryHeap()
for v in array_grande:
    heap_insert.insert(v)
trocas_insert = len(heap_insert.trocas)

print(f"Build_heap: {trocas_build:>3} trocas -> {heap_build._dados}")
print(f"Inserções individuais: {trocas_insert:>3} trocas -> {heap_insert._dados}")
print(f"Build_heap produziu {trocas_insert - trocas_build} trocas a menos")
print(f"Ambas as heaps são válidas: {is_valid_heap(heap_build._dados) and is_valid_heap(heap_insert._dados)}\n")
