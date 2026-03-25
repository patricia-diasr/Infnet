from typing import Any, List, Optional, Tuple
import random
import math


class StackOverflowError(Exception):
    """Levantada ao tentar inserir em uma Stack que já atingiu capacidade máxima"""


class StackUnderflowError(Exception):
    """Levantada ao tentar remover de uma Stack vazia"""


class QueueOverflowError(Exception):
    """Levantada ao tentar inserir em uma Queue que já atingiu capacidade máxima"""


class QueueUnderflowError(Exception):
    """Levantada ao tentar remover de uma Queue vazia"""


class Stack:
    """
    Pilha com capacidade fixa baseada em array

    Attributes:
        capacidade (int): Número máximo de elementos suportados
        _dados (List): Array interno pré-alocado
        _topo (int): Índice do elemento no topo, -1 se vazia
    """

    def __init__(self, capacidade: int) -> None:
        if capacidade <= 0:
            raise ValueError(f"Capacidade deve ser positiva, recebido: {capacidade}")

        self.capacidade: int = capacidade
        self._dados: List[Any] = [None] * capacidade
        self._topo: int = -1

    def push(self, valor: Any) -> None:
        """
        Insere um elemento no topo da pilha

        Args:
            valor: Elemento a ser inserido

        Raises:
            StackOverflowError: Se a pilha já está na capacidade máxima
        """

        if self._topo == self.capacidade - 1:
            raise StackOverflowError(f"Stack overflow: capacidade máxima ({self.capacidade}) atingida")

        self._topo += 1
        self._dados[self._topo] = valor

    def pop(self) -> Any:
        """
        Remove e retorna o elemento do topo da pilha

        Returns:
            Elemento removido do topo

        Raises:
            StackUnderflowError: Se a pilha está vazia
        """

        if self._topo == -1:
            raise StackUnderflowError("Stack underflow: pilha vazia")

        valor = self._dados[self._topo]
        self._dados[self._topo] = None
        self._topo -= 1

        return valor

    def peek(self) -> Any:
        """
        Retorna o elemento do topo sem remover

        Returns:
            Elemento no topo

        Raises:
            StackUnderflowError: Se a pilha está vazia
        """

        if self._topo == -1:
            raise StackUnderflowError("Stack underflow: pilha vazia")

        return self._dados[self._topo]

    def esta_vazia(self) -> bool:
        return self._topo == -1

    def esta_cheia(self) -> bool:
        return self._topo == self.capacidade - 1

    def __len__(self) -> int:
        return self._topo + 1

    def __repr__(self) -> str:
        elementos = self._dados[: self._topo + 1]
        return f"Stack(topo->{elementos[::-1]})"


class Queue:
    """
    Fila com capacidade fixa baseada em array circular

    Attributes:
        capacidade (int): Número máximo de elementos suportados
        _dados (List): Array interno pré-alocado com capacidade + 1 slots
        _frente (int): Índice do próximo elemento a ser removido
        _fim (int): Índice onde o próximo elemento será inserido
        _tamanho (int): Número atual de elementos
    """

    def __init__(self, capacidade: int) -> None:
        if capacidade <= 0:
            raise ValueError(f"Capacidade deve ser positiva, recebido: {capacidade}")
        
        self.capacidade: int = capacidade
        self._dados: List[Any] = [None] * capacidade
        self._frente: int = 0
        self._fim: int = 0
        self._tamanho: int = 0

    def enqueue(self, valor: Any) -> None:
        """
        Insere um elemento no final da fila

        Args:
            valor: Elemento a ser inserido

        Raises:
            QueueOverflowError: Se a fila já está na capacidade máxima
        """

        if self._tamanho == self.capacidade:
            raise QueueOverflowError(f"Queue overflow: capacidade máxima ({self.capacidade}) atingida")

        self._dados[self._fim] = valor
        self._fim = (self._fim + 1) % self.capacidade
        self._tamanho += 1

    def dequeue(self) -> Any:
        """
        Remove e retorna o elemento da frente da fila

        Returns:
            Elemento removido da frente

        Raises:
            QueueUnderflowError: Se a fila está vazia
        """

        if self._tamanho == 0:
            raise QueueUnderflowError("Queue underflow: fila vazia")
        
        valor = self._dados[self._frente]
        self._dados[self._frente] = None
        self._frente = (self._frente + 1) % self.capacidade
        self._tamanho -= 1

        return valor

    def front(self) -> Any:
        """
        Retorna o elemento da frente sem removê-lo

        Returns:
            Elemento na frente da fila

        Raises:
            QueueUnderflowError: Se a fila está vazia
        """

        if self._tamanho == 0:
            raise QueueUnderflowError("Queue underflow: fila vazia")
        
        return self._dados[self._frente]

    def esta_vazia(self) -> bool:
        return self._tamanho == 0

    def esta_cheia(self) -> bool:
        return self._tamanho == self.capacidade

    def __len__(self) -> int:
        return self._tamanho

    def __repr__(self) -> str:
        if self._tamanho == 0:
            return "Queue(frente->[])"

        elementos = []
        i = self._frente

        for _ in range(self._tamanho):
            elementos.append(self._dados[i])
            i = (i + 1) % self.capacidade

        return f"Queue(frente->{elementos})"


class NoBST:
    """
    Nó de uma Árvore Binária de Busca

    Attributes:
        valor (int): Valor numérico do nó
        esquerda (Optional[NoBST]): Filho à esquerda
        direita (Optional[NoBST]): Filho à direita
    """

    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.esquerda: Optional["NoBST"] = None
        self.direita: Optional["NoBST"] = None


class BinarySearchTree:
    """
    Árvore Binária de Busca para demonstração de travessias

    Attributes:
        raiz (Optional[NoBST]): Raiz da árvore
        total_nos (int): Número total de nós
    """

    def __init__(self) -> None:
        self.raiz: Optional[NoBST] = None
        self.total_nos: int = 0

    def inserir(self, valor: int) -> None:
        """
        Insere um valor na posição correta da BST

        Args:
            valor (int): Inteiro a ser inserido
        """

        novo = NoBST(valor)

        if self.raiz is None:
            self.raiz = novo

        else:
            atual = self.raiz

            while True:
                if valor < atual.valor:
                    if atual.esquerda is None:
                        atual.esquerda = novo
                        break

                    atual = atual.esquerda

                else:
                    if atual.direita is None:
                        atual.direita = novo
                        break

                    atual = atual.direita

        self.total_nos += 1


def atravessamento_amplitude(bst: BinarySearchTree) -> List[int]:
    """
    Realiza o atravessamento em nível (BFS) utilizando a classe Queue personalizada

    Args:
        bst (BinarySearchTree): Árvore a ser percorrida

    Returns:
        List[int]: Valores visitados em ordem de nível
    """

    if bst.raiz is None:
        return []

    resultado: List[int] = []
    fila = Queue(capacidade=bst.total_nos)
    fila.enqueue(bst.raiz)

    while not fila.esta_vazia():
        no = fila.dequeue()
        resultado.append(no.valor)

        if no.esquerda:
            fila.enqueue(no.esquerda)

        if no.direita:
            fila.enqueue(no.direita)

    return resultado


def atravessamento_profundidade(bst: BinarySearchTree) -> List[int]:
    """
    Realiza o atravessamento por caminhos (DFS) utilizando a classe Stack personalizada

    Args:
        bst (BinarySearchTree): Árvore a ser percorrida

    Returns:
        List[int]: Valores visitados em profundidade (Pre-order)
    """

    if bst.raiz is None:
        return []

    resultado: List[int] = []
    pilha = Stack(capacidade=bst.total_nos)
    pilha.push(bst.raiz)

    while not pilha.esta_vazia():
        no = pilha.pop()
        resultado.append(no.valor)

        if no.direita:
            pilha.push(no.direita)

        if no.esquerda:
            pilha.push(no.esquerda)

    return resultado

random.seed(42)
n_elementos = 8
elementos = random.sample(range(1, 100), n_elementos)

bst = BinarySearchTree()
for e in elementos:
    bst.inserir(e)

print(f"\n===== Teste 1 - Árvore Populada =====\n")
print(f"Elementos (ordem de inserção): {elementos}")

print("\n\n===== Teste 2 - Atravessamento em Amplitude (Fila) =====\n")
res_bfs = atravessamento_amplitude(bst)
print(f"Resultado BFS: {res_bfs}")

print("\n\n===== Teste 3 - Atravessamento em Profundidade (Pilha) =====\n")
res_dfs = atravessamento_profundidade(bst)
print(f"Resultado DFS: {res_dfs}")

print("\n\n===== Teste 4 - Validação de Robustez das Estruturas =====\n")

try:
    print("Tentando estourar a capacidade da Stack...")
    s = Stack(capacidade=2)
    s.push(1); s.push(2); s.push(3)

except StackOverflowError as e:
    print(f"=> Sucesso ao capturar erro: {e}")

try:
    print("\nTentando remover de uma Queue vazia...")
    q = Queue(capacidade=5)
    q.dequeue()

except QueueUnderflowError as e:
    print(f"=> Sucesso ao capturar erro: {e}")
    