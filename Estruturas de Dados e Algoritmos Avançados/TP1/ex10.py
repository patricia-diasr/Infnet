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


def k_maiores(array: List[int], k: int) -> List[int]:
    """
    Extrai os k maiores elementos de um array utilizando heap binária máxima

    Args:
        array (List[int]): Array de entrada
        k (int): Quantidade de maiores elementos a extrair

    Returns:
        List[int]: Lista com os k maiores elementos em ordem decrescente

    Raises:
        ValueError: Se k for negativo ou maior que o tamanho do array
    """

    if k < 0 or k > len(array):
        raise ValueError(f"k inválido: esperado entre 0 e {len(array)}, recebido {k}")

    heap = BinaryHeap()
    heap.build_heap(array)
    resultado: List[int] = []

    for _ in range(k):
        resultado.append(heap.extract_max())

    return resultado


print("\n===== Teste 1 - k Maiores Elementos (casos básicos) =====\n")

random.seed(42)
array_base = random.sample(range(1, 100), 15)
referencia = sorted(array_base, reverse=True)

print(f"Array: {array_base}")
print(f"Ordenado: {referencia}\n")

for k in [1, 3, 5, 10, 15]:
    resultado = k_maiores(array_base, k)
    correto = resultado == referencia[:k]
    status = "OK" if correto else "FALHOU"
    print(f"[{status}] k = {k:>2} -> {resultado}")


print("\n\n===== Teste 2 - k Maiores com Diferentes Tamanhos de Array =====\n")

random.seed(42)
casos = [
    (random.sample(range(1, 50),   10),  3),
    (random.sample(range(1, 200),  50),  10),
    (random.sample(range(1, 1000), 100), 5),
]

for array, k in casos:
    resultado = k_maiores(array, k)
    referencia = sorted(array, reverse=True)[:k]
    correto = resultado == referencia
    status = "OK" if correto else "FALHOU"
    print(f"[{status}] n = {len(array):>3}, k = {k:>2} -> {resultado}")


print("\n\n===== Teste 3 - Robustez: valores inválidos de k =====\n")

array_teste = [5, 3, 8, 1, 9]

for k_invalido in [-1, 6, 100]:
    try:
        k_maiores(array_teste, k_invalido)
    except ValueError as e:
        print(f"=> Sucesso ao capturar erro (k={k_invalido}): {e}")


print("\n\n===== Teste 4 - Casos Limite: k=0 e k=n =====\n")

array_limite = [4, 10, 3, 5, 1, 8, 2]
resultado_zero = k_maiores(array_limite, 0)
resultado_n = k_maiores(array_limite, len(array_limite))

print(f"k = 0 -> {resultado_zero} (Lista vazia esperada)")
print(f"k = n -> {resultado_n} (Todos os elementos em ordem decrescente)\n")
