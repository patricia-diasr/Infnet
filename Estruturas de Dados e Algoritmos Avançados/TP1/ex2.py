from typing import List, Tuple


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


    def __len__(self) -> int:
        return len(self._dados)


    def __repr__(self) -> str:
        return f"BinaryHeap(raiz={self._dados[0] if self._dados else None}, dados={self._dados})"


print("\n===== Teste 1 - Funções Auxiliares de Índice =====\n")

heap = BinaryHeap()

for i in range(7):
        print(f"nó[{i}] -> pai = {heap.indice_pai(i) if i > 0 else '-':>2},  filho_esq = {heap.indice_filho_esquerdo(i):>2},  filho_dir = {heap.indice_filho_direito(i):>2}")
print()
