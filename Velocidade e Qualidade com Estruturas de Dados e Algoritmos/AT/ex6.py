from typing import Any, Iterator, List, Optional, Tuple


class IndiceInvalidoError(Exception):
    """Levantada quando o índice fornecido está fora dos limites da lista"""


class ValorNaoEncontradoError(Exception):
    """Levantada quando o valor alvo não existe na lista"""


class No:
    """
    Nó de uma lista simplesmente encadeada

    Attributes:
        valor: Dado armazenado no nó
        proximo (Optional[No]): Referência ao próximo nó da cadeia
    """

    def __init__(self, valor: Any) -> None:
        self.valor: Any = valor
        self.proximo: Optional["No"] = None

    def __repr__(self) -> str:
        return f"No({self.valor!r})"


class SinglyLinkedList:
    """
    Lista simplesmente encadeada com suporte a operações por posição

    Attributes:
        _cabeca (Optional[No]): Primeiro nó da lista
        _cauda (Optional[No]): Último nó da lista (ponteiro de cauda)
        _tamanho (int): Número de elementos armazenados
    """

    def __init__(self) -> None:
        self._cabeca: Optional[No] = None
        self._cauda: Optional[No] = None
        self._tamanho: int = 0

    def insert_first(self, valor: Any) -> None:
        """
        Insere um elemento no início da lista

        Args:
            valor: Elemento a inserir
        """

        novo = No(valor)
        novo.proximo = self._cabeca
        self._cabeca = novo
        
        if self._cauda is None:
            self._cauda = novo
        
        self._tamanho += 1

    def insert_last(self, valor: Any) -> None:
        """
        Insere um elemento no final da lista usando ponteiro de cauda

        Args:
            valor: Elemento a inserir
        """

        novo = No(valor)

        if self._cauda is None:
            self._cabeca = novo
            self._cauda = novo

        else:
            self._cauda.proximo = novo
            self._cauda = novo

        self._tamanho += 1

    def search(self, valor: Any) -> int:
        """
        Busca um valor na lista e retorna seu índice

        Args:
            valor: Valor a localizar

        Returns:
            int: Índice da primeira ocorrência encontrada

        Raises:
            ValorNaoEncontradoError: Se o valor não existir na lista
        """

        atual = self._cabeca
        indice = 0

        while atual is not None:
            if atual.valor == valor:
                return indice
        
            atual = atual.proximo
            indice += 1

        raise ValorNaoEncontradoError(f"Valor {valor!r} não encontrado na lista")

    def delete(self, valor: Any) -> None:
        """
        Remove a primeira ocorrência do valor especificado

        Args:
            valor: Valor a ser removido

        Raises:
            ValorNaoEncontradoError: Se a lista estiver vazia ou o valor não existir
        """

        if self._cabeca is None:
            raise ValorNaoEncontradoError("Impossível remover: lista vazia")

        if self._cabeca.valor == valor:
            self._cabeca = self._cabeca.proximo
            
            if self._cabeca is None:
                self._cauda = None
            
            self._tamanho -= 1
            return

        anterior = self._cabeca
        atual = self._cabeca.proximo

        while atual is not None:
            if atual.valor == valor:
                anterior.proximo = atual.proximo
                
                if atual.proximo is None:
                    self._cauda = anterior
                
                self._tamanho -= 1
                return
            
            anterior = atual
            atual = atual.proximo

        raise ValorNaoEncontradoError(f"Valor {valor!r} não encontrado na lista")

    def insert_at(self, indice: int, valor: Any) -> None:
        """
        Insere um elemento em uma posição arbitrária

        Args:
            indice (int): Posição de inserção
            valor: Elemento a inserir

        Raises:
            IndiceInvalidoError: Se o índice estiver fora do intervalo permitido
        """

        if not 0 <= indice <= self._tamanho:
            raise IndiceInvalidoError(f"Índice {indice} inválido (Tamanho atual: {self._tamanho})")
        
        if indice == 0:
            self.insert_first(valor)
            return
        
        if indice == self._tamanho:
            self.insert_last(valor)
            return

        atual = self._cabeca
        for _ in range(indice - 1):
            atual = atual.proximo

        novo = No(valor)
        novo.proximo = atual.proximo
        atual.proximo = novo
        self._tamanho += 1

    def delete_at(self, indice: int) -> Any:
        """
        Remove e retorna o elemento na posição especificada

        Args:
            indice (int): Posição do elemento a remover

        Returns:
            Any: Valor do elemento removido

        Raises:
            IndiceInvalidoError: Se o índice for negativo ou >= tamanho
        """

        if not 0 <= indice < self._tamanho:
            raise IndiceInvalidoError(f"Índice {indice} inválido (Tamanho atual: {self._tamanho})")

        if indice == 0:
            valor = self._cabeca.valor
            self._cabeca = self._cabeca.proximo
        
            if self._cabeca is None:
                self._cauda = None
        
            self._tamanho -= 1
            return valor

        anterior = self._cabeca
        for _ in range(indice - 1):
            anterior = anterior.proximo

        alvo = anterior.proximo
        anterior.proximo = alvo.proximo
        
        if alvo.proximo is None:
            self._cauda = anterior
        
        self._tamanho -= 1
        return alvo.valor

    def __len__(self) -> int:
        return self._tamanho

    def __str__(self) -> str:        
        partes = [repr(v) for v in self]
        return "head -> " + " -> ".join(partes) + " -> None"

    def __iter__(self) -> Iterator[Any]:        
        atual = self._cabeca
        while atual:
            yield atual.valor
            atual = atual.proximo


print("\n===== Teste 1 - Inserções Básicas e Invariantes =====\n")

lista = SinglyLinkedList()
print(f"Estado inicial: {lista}, len={len(lista)}")

lista.insert_last(20)
lista.insert_first(10)
lista.insert_last(30)

print(f"Após inserções (10, 20, 30): {lista}")
print(f"Verificação de tamanho: {len(lista)}")


print("\n\n===== Teste 2 - Operações por Posição (insert_at / delete_at) =====\n")

print(f"Antes do insert_at(1, 15): {lista}")
lista.insert_at(1, 15)
print(f"Depois do insert_at(1, 15): {lista}")

indice_alvo = 3
val_removido = lista.delete_at(indice_alvo)
print(f"=> delete_at({indice_alvo}) -> valor removido: {val_removido}")
print(f"Estado atual: {lista}")


print("\n\n===== Teste 3 - Busca e Remoção por Valor =====\n")

try:
    alvo = 20
    idx = lista.search(alvo)
    print(f"=> search({alvo}) -> encontrado no índice: {idx}")
    
    lista.delete(alvo)
    print(f"=> delete({alvo}) -> nova lista: {lista}")
    
except (ValorNaoEncontradoError, IndiceInvalidoError) as e:
    print(f"Erro inesperado: {e}")


print("\n\n===== Teste 4 - Tratamento de Exceções (Casos Inválidos) =====\n")

try:
    print(f"Tentando insert_at(100, 99) em lista de tamanho {len(lista)}...")
    lista.insert_at(100, 99)
except IndiceInvalidoError as e:
    print(f"=> Sucesso ao capturar erro esperado: {e}")

try:
    print("\nTentando buscar valor que não está na lista (999)...")
    lista.search(999)
except ValorNaoEncontradoError as e:
    print(f"=> Sucesso ao capturar erro esperado: {e}")
