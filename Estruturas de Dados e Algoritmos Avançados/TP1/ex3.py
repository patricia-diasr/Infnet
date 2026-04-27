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


    def insert(self, valor: int) -> None:
        """
        Insere um valor na heap preservando todas as invariantes

        Args:
            valor (int): Valor inteiro a ser inserido
        """

        self._dados.append(valor)
        self._sift_up(len(self._dados) - 1)


    def __len__(self) -> int:
        return len(self._dados)


    def __repr__(self) -> str:
        return f"BinaryHeap(raiz={self._dados[0] if self._dados else None}, dados={self._dados})"


print("\n===== Teste 1 - Inserção em Ordem Crescente =====\n")

heap_crescente = BinaryHeap()
sequencia_crescente = [1, 2, 3, 4, 5, 6, 7]

for v in sequencia_crescente:
    heap_crescente.insert(v)
    print(f"=> insert({v}) -> {heap_crescente._dados}")

print(f"\nTrocas realizadas ({len(heap_crescente.trocas)} no total):")
for troca in heap_crescente.trocas:
    print(f"=> Índice {troca[0]} (valor {troca[1]}) <-> Índice {troca[2]} (valor {troca[3]})")


print("\n\n===== Teste 2 - Inserção em Ordem Decrescente =====\n")

heap_decrescente = BinaryHeap()
sequencia_decrescente = [7, 6, 5, 4, 3, 2, 1]

for v in sequencia_decrescente:
    heap_decrescente.insert(v)
    print(f"=> insert({v}) -> {heap_decrescente._dados}")

print(f"\nTrocas realizadas ({len(heap_decrescente.trocas)} no total):")
for troca in heap_decrescente.trocas:
    print(f"=> Índice {troca[0]} (valor {troca[1]}) <-> Índice {troca[2]} (valor {troca[3]})")


print("\n\n===== Teste 3 - Inserção em Ordem Aleatória =====\n")

heap_aleatorio = BinaryHeap()
sequencia_aleatoria = [4, 10, 3, 5, 1, 8, 2]

for v in sequencia_aleatoria:
    heap_aleatorio.insert(v)
    print(f"=> insert({v}) -> {heap_aleatorio._dados}")

print(f"\nTrocas realizadas ({len(heap_aleatorio.trocas)} no total):")
for troca in heap_aleatorio.trocas:
    print(f"=> Índice {troca[0]} (valor {troca[1]}) <-> Índice {troca[2]} (valor {troca[3]})")

print(f"\nEstado final: {heap_aleatorio}\n")
