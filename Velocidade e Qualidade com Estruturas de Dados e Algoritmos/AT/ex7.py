from typing import Any, Iterator, List, Optional, Tuple


class DequeVazioError(Exception):
    """Levantada ao tentar remover ou consultar elemento de um Deque vazio"""


class InvarianteVioladoError(Exception):
    """Levantada quando uma verificação de invariante estrutural falha"""


class NoDuplo:
    """
    Nó de uma lista duplamente encadeada

    Attributes:
        valor: Dado armazenado no nó
        anterior (Optional[NoDuplo]): Referência ao nó predecessor
        proximo (Optional[NoDuplo]): Referência ao nó sucessor
    """

    def __init__(self, valor: Any) -> None:
        self.valor: Any = valor
        self.anterior: Optional["NoDuplo"] = None
        self.proximo: Optional["NoDuplo"] = None

    def __repr__(self) -> str:
        return f"NoDuplo({self.valor!r})"


class DoublyLinkedList:
    """
    Lista duplamente encadeada utilizando sentinelas de cabeça e cauda

    Attributes:
        _sentinela_cabeca (NoDuplo): Marcador fixo do início da lista
        _sentinela_cauda (NoDuplo): Marcador fixo do fim da lista
        _tamanho (int): Número de nós de dados (excluindo sentinelas)
    """

    def __init__(self) -> None:
        self._sentinela_cabeca: NoDuplo = NoDuplo(None)
        self._sentinela_cauda: NoDuplo = NoDuplo(None)
        self._sentinela_cabeca.proximo = self._sentinela_cauda
        self._sentinela_cauda.anterior = self._sentinela_cabeca
        self._tamanho: int = 0

    def insert_first(self, valor: Any) -> None:
        """
        Insere um novo valor no início da lista

        Args:
            valor: Elemento a inserir
        """

        self._insert_between(self._sentinela_cabeca, self._sentinela_cabeca.proximo, valor)

    def insert_last(self, valor: Any) -> None:
        """
        Insere um novo valor no final da lista

        Args:
            valor: Elemento a inserir
        """
        
        self._insert_between(self._sentinela_cauda.anterior, self._sentinela_cauda, valor)

    def delete_first(self) -> Any:
        """
        Remove e retorna o primeiro elemento de dados

        Returns:
            Any: Valor do nó removido

        Raises:
            DequeVazioError: Se a lista estiver vazia
        """
        
        if self.is_empty():
            raise DequeVazioError("Impossível remover: lista vazia")
        
        return self._remove_at(self._sentinela_cabeca.proximo)

    def delete_last(self) -> Any:
        """
        Remove e retorna o último elemento de dados

        Returns:
            Any: Valor do nó removido

        Raises:
            DequeVazioError: Se a lista estiver vazia
        """

        if self.is_empty():
            raise DequeVazioError("Impossível remover: lista vazia")
        
        return self._remove_at(self._sentinela_cauda.anterior)

    def is_empty(self) -> bool:
        """
        Verifica se a lista contém elementos de dados

        Returns:
            bool: True se vazia, False caso contrário
        """

        return self._tamanho == 0

    def _insert_between(self, anterior: NoDuplo, proximo: NoDuplo, valor: Any) -> None:
        """
        Método auxiliar para encadear um novo nó entre dois nós existentes

        Args:
            anterior: Nó que precederá o novo nó
            proximo: Nó que sucederá o novo nó
            valor: Valor a ser inserido
        """
        
        novo = NoDuplo(valor)
        novo.anterior = anterior
        novo.proximo = proximo
        anterior.proximo = novo
        proximo.anterior = novo
        self._tamanho += 1

    def _remove_at(self, no: NoDuplo) -> Any:
        """
        Método auxiliar para desconectar um nó da cadeia

        Args:
            no: Nó de dados a ser removido

        Returns:
            Any: Valor armazenado no nó removido
        """
        
        anterior = no.anterior
        proximo = no.proximo
        anterior.proximo = proximo
        proximo.anterior = anterior
        valor = no.valor
        
        no.anterior = no.proximo = None
        self._tamanho -= 1
        return valor

    def verificar_invariantes(self) -> None:
        """
        Valida a integridade estrutural da lista (ponteiros e tamanho)

        Raises:
            InvarianteVioladoError: Se houver inconsistência nos ponteiros ou contagem
        """

        atual = self._sentinela_cabeca
        contagem = 0

        while atual.proximo is not None:
            proximo = atual.proximo

            if proximo.anterior is not atual:
                raise InvarianteVioladoError(f"Ponteiro quebrado entre {atual} e {proximo}")

            atual = proximo

            if atual is not self._sentinela_cauda:
                contagem += 1
        
        if contagem != self._tamanho:
            raise InvarianteVioladoError(f"Tamanho inconsistente: esperado {self._tamanho}, contado {contagem}")

    def __len__(self) -> int:
        return self._tamanho

    def __iter__(self) -> Iterator[Any]:
        atual = self._sentinela_cabeca.proximo

        while atual is not self._sentinela_cauda:
            yield atual.valor
            atual = atual.proximo

    def __str__(self) -> str:
        valores = [repr(v) for v in self]
        return "None <-> " + " <-> ".join(valores) + " <-> None"


class Deque:
    """
    Double-Ended Queue (Deque) implementado sobre uma DoublyLinkedList

    Attributes:
        _lista (DoublyLinkedList): Estrutura duplamente encadeada subjacente
    """

    def __init__(self) -> None:
        self._lista: DoublyLinkedList = DoublyLinkedList()

    def insert_left(self, valor: Any) -> None:
        """
        Insere um elemento na extremidade esquerda (início) do deque

        Args:
            valor: Elemento a ser inserido.
        """

        self._lista.insert_first(valor)

    def insert_right(self, valor: Any) -> None:
        """
        Insere um elemento na extremidade direita (fim) do deque

        Args:
            valor: Elemento a ser inserido
        """
        
        self._lista.insert_last(valor)

    def remove_left(self) -> Any:
        """
        Remove e retorna o elemento da extremidade esquerda

        Returns:
            Any: O valor do elemento removido

        Raises:
            DequeVazioError: Se o deque estiver vazio
        """
        
        try:
            return self._lista.delete_first()
        
        except DequeVazioError:
            raise DequeVazioError("Erro em remove_left: Deque está vazio")

    def remove_right(self) -> Any:
        """
        Remove e retorna o elemento da extremidade direita

        Returns:
            Any: O valor do elemento removido

        Raises:
            DequeVazioError: Se o deque estiver vazio
        """

        try:
            return self._lista.delete_last()
        
        except DequeVazioError:
            raise DequeVazioError("Erro em remove_right: Deque está vazio")

    def peek_left(self) -> Any:
        """
        Retorna o valor do elemento à esquerda sem removê-lo

        Returns:
            Any: Valor do primeiro elemento

        Raises:
            DequeVazioError: Se o deque estiver vazio
        """

        if self.is_empty():
            raise DequeVazioError("Erro em peek_left: Deque está vazio")
        
        return self._lista._sentinela_cabeca.proximo.valor

    def peek_right(self) -> Any:
        """
        Retorna o valor do elemento à direita sem removê-lo

        Returns:
            Any: Valor do último elemento

        Raises:
            DequeVazioError: Se o deque estiver vazio
        """

        if self.is_empty():
            raise DequeVazioError("Erro em peek_right: Deque está vazio")
        
        return self._lista._sentinela_cauda.anterior.valor

    def is_empty(self) -> bool:
        """
        Verifica se o deque não possui elementos

        Returns:
            bool: True se vazio, False caso contrário
        """

        return self._lista.is_empty()

    def verificar_invariantes(self) -> None:
        """
        Valida a integridade da estrutura interna delegando à lista

        Raises:
            InvarianteVioladoError: Se houver falha estrutural nos ponteiros
        """

        self._lista.verificar_invariantes()

    def __len__(self) -> int:
        return len(self._lista)

    def __str__(self) -> str:
        elementos = [repr(v) for v in self._lista]
        return "<-[ " + " | ".join(elementos) + " ]->"


print("\n===== Teste 1 - Deque: Bateria de Inserções e Remoções Alternadas =====\n")

dq = Deque()
print(f"Estado inicial: {dq}, len={len(dq)}")

dq.insert_right("B")
dq.insert_left("A")
dq.insert_right("C")
print(f"Após inserir A (esq), B e C (dir): {dq}")

dq.verificar_invariantes()
print("✅ Invariantes validados após inserções.")

v_esq = dq.remove_left()
v_dir = dq.remove_right()
print(f"\nRemovido esq: {v_esq} | Removido dir: {v_dir}")
print(f"Estado final: {dq}")


print("\n\n===== Teste 2 - Sequência Longa e Estresse de Invariantes =====\n")

dq_stress = Deque()
print("Executando 10 inserções alternadas...")

for i in range(1, 6):
    dq_stress.insert_left(i)
    dq_stress.insert_right(i * 10)

print(f"Deque resultante: {dq_stress}")
dq_stress.verificar_invariantes()

print("\nEsvaziando deque pelas duas pontas...")
while not dq_stress.is_empty():
    dq_stress.remove_left()

    if not dq_stress.is_empty():
        dq_stress.remove_right()
    
    dq_stress.verificar_invariantes()

print(f"Estado após esvaziamento: {dq_stress}, len={len(dq_stress)}")
print("✅ Invariantes estruturais mantidos durante todo o ciclo")
