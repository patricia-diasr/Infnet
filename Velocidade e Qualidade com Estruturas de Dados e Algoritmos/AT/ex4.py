from typing import Any, List, Optional, Tuple
import random
import math


class NoBucket:
    """
    Nó de uma lista encadeada que armazena um par (chave, valor)

    Attributes:
        chave: Chave de identificação do par
        valor: Valor associado à chave
        proximo (Optional[NoBucket]): Próximo nó na cadeia do bucket
    """

    def __init__(self, chave: Any, valor: Any) -> None:
        self.chave: Any = chave
        self.valor: Any = valor
        self.proximo: Optional["NoBucket"] = None


class ListaBucket:
    """
    Lista encadeada de pares (chave, valor) usada como bucket da HashTable

    Attributes:
        cabeca (Optional[NoBucket]): Primeiro nó da cadeia
        tamanho (int): Número de pares armazenados neste bucket
    """

    def __init__(self) -> None:
        self.cabeca: Optional[NoBucket] = None
        self.tamanho: int = 0

    def buscar(self, chave: Any) -> Tuple[Optional[Any], int]:
        """
        Busca o valor associado a uma chave percorrendo a cadeia

        Args:
            chave: Chave a ser localizada

        Returns:
            Tuple[Optional[Any], int]:
                - valor encontrado ou None se ausente
                - número de comparações realizadas
        """

        comparacoes = 0
        atual = self.cabeca
        while atual is not None:
            comparacoes += 1
            
            if atual.chave == chave:
                return atual.valor, comparacoes
            
            atual = atual.proximo

        return None, comparacoes

    def inserir_ou_atualizar(self, chave: Any, valor: Any) -> Tuple[bool, int]:
        """
        Insere um novo par ou atualiza o valor de uma chave já existente

        Args:
            chave: Chave do par
            valor: Valor a ser associado

        Returns:
            Tuple[bool, int]:
                - True se foi uma inserção nova, False se foi atualização
                - número de comparações realizadas
        """

        comparacoes = 0
        atual = self.cabeca

        while atual is not None:
            comparacoes += 1
        
            if atual.chave == chave:
                atual.valor = valor
                return False, comparacoes
        
            atual = atual.proximo

        novo = NoBucket(chave, valor)
        novo.proximo = self.cabeca
        
        self.cabeca = novo
        self.tamanho += 1
        
        return True, comparacoes

    def remover(self, chave: Any) -> Tuple[bool, int]:
        """
        Remove o nó com a chave especificada da cadeia

        Args:
            chave: Chave do par a ser removido

        Returns:
            Tuple[bool, int]:
                - True se a chave foi encontrada e removida, False se ausente
                - número de comparações realizadas
        """

        comparacoes = 0
        anterior = None
        atual = self.cabeca

        while atual is not None:
            comparacoes += 1
        
            if atual.chave == chave:
        
                if anterior is None:
                    self.cabeca = atual.proximo
        
                else:
                    anterior.proximo = atual.proximo
        
                self.tamanho -= 1
                return True, comparacoes
        
            anterior = atual
            atual = atual.proximo

        return False, comparacoes

    def pares(self) -> List[Tuple[Any, Any]]:
        """
        Retorna todos os pares (chave, valor) presentes neste bucket

        Returns:
            List[Tuple[Any, Any]]: Lista de pares na ordem da cadeia
        """

        resultado = []
        atual = self.cabeca
        
        while atual is not None:
            resultado.append((atual.chave, atual.valor))
            atual = atual.proximo
        
        return resultado


class HashTableChained:
    """
    Tabela hash com resolução de colisões por encadeamento (chaining)

    Attributes:
        capacidade (int): Número atual de buckets
        limiar_carga (float): Fator de carga que dispara o rehash
        total_elementos (int): Total de pares armazenados
        total_comparacoes (int): Acumulador de comparações nas operações
        total_rehashes (int): Contador de rehashes realizados
        _buckets (List[ListaBucket]): Array interno de bucketso
    """

    CAPACIDADE_INICIAL = 11
    LIMIAR_CARGA_PADRAO = 0.75

    def __init__(self, capacidade_inicial: int = CAPACIDADE_INICIAL, limiar_carga: float = LIMIAR_CARGA_PADRAO) -> None:
        self.capacidade: int = capacidade_inicial
        self.limiar_carga: float = limiar_carga
        self.total_elementos: int = 0
        self.total_comparacoes: int = 0
        self.total_rehashes: int = 0
        self._buckets: List[ListaBucket] = self.criar_buckets(self.capacidade)


    def put(self, chave: Any, valor: Any) -> None:
        """
        Insere ou atualiza o par (chave, valor) na tabela

        Args:
            chave: Chave do par (deve ser hashável)
            valor: Valor a ser associado à chave
        """

        indice = self._hash(chave)
        foi_insercao, comparacoes = self._buckets[indice].inserir_ou_atualizar(chave, valor)
        self.total_comparacoes += comparacoes

        if foi_insercao:
            self.total_elementos += 1

            if self.fator_carga() > self.limiar_carga:
                self._rehash()

    def get(self, chave: Any) -> Optional[Any]:
        """
        Retorna o valor associado à chave ou None se ausente

        Args:
            chave: Chave a ser consultada

        Returns:
            Valor encontrado ou None
        """

        indice = self._hash(chave)
        valor, comparacoes = self._buckets[indice].buscar(chave)

        self.total_comparacoes += comparacoes
        return valor

    def delete(self, chave: Any) -> bool:
        """
        Remove o par com a chave especificada da tabela

        Args:
            chave: Chave do par a remover

        Returns:
            bool: True se removido, False se a chave não existia
        """

        indice = self._hash(chave)
        removido, comparacoes = self._buckets[indice].remover(chave)
        self.total_comparacoes += comparacoes

        if removido:
            self.total_elementos -= 1

        return removido

    def __len__(self) -> int:
        return self.total_elementos

    def __contains__(self, chave: Any) -> bool:
        return self.get(chave) is not None

    def fator_carga(self) -> float:
        """Retorna o fator de carga atual: n / capacidade"""

        return self.total_elementos / self.capacidade

    def distribuicao_buckets(self) -> List[int]:
        """
        Retorna o tamanho de cada bucket, útil para análise de distribuição

        Returns:
            List[int]: Comprimento de cada cadeia no array de buckets
        """

        return [b.tamanho for b in self._buckets]

    def resetar_contadores(self) -> None:
        """Zera os acumuladores de comparações sem alterar os dados"""

        self.total_comparacoes = 0

    def _hash(self, chave: Any) -> int:
        """Mapeia uma chave para um índice válido do array de buckets"""

        return hash(chave) % self.capacidade

    @staticmethod
    def criar_buckets(capacidade: int) -> List[ListaBucket]:
        return [ListaBucket() for _ in range(capacidade)]

    @staticmethod
    def proximo_primo(n: int) -> int:
        """
        Retorna o menor número primo maior ou igual a n
        
        Args:
            n (int): Limite inferior

        Returns:
            int: Menor primo >= n
        """
        
        def e_primo(x: int) -> bool:
            if x < 2:
                return False
            
            if x == 2:
                return True
            
            if x % 2 == 0:
                return False
            
            for i in range(3, int(math.sqrt(x)) + 1, 2):
                if x % i == 0:
                    return False
            
            return True

        candidato = n if n % 2 != 0 else n + 1
        
        while not e_primo(candidato):
            candidato += 2
        
        return candidato

    def _rehash(self) -> None:
        """
        Redimensiona a tabela para a próxima capacidade prima acima do dobro da capacidade atual e reinsere todos os pares existentes
        """

        nova_capacidade = self.proximo_primo(self.capacidade * 2 + 1)
        novos_buckets = self.criar_buckets(nova_capacidade)

        for bucket in self._buckets:
            for chave, valor in bucket.pares():
                novo_indice = hash(chave) % nova_capacidade
                novos_buckets[novo_indice].inserir_ou_atualizar(chave, valor)

        self._buckets = novos_buckets
        self.capacidade = nova_capacidade
        self.total_rehashes += 1


random.seed(42)


print("\n===== Teste 1 - Operações básicas =====\n")

tabela = HashTableChained()
operacoes = [
    ("put", "nome", "Maria"),
    ("put", "idade", 30),
    ("put", "cidade", "Tatuí"),
    ("get", "nome", None),
    ("get", "ausente", None),
    ("put", "nome", "João"),
    ("get", "nome", None),
    ("delete", "idade", None),
    ("get", "idade", None),
    ("delete", "inexistente", None),
]

for op, chave, valor in operacoes:
    if op == "put":
        tabela.put(chave, valor)
        print(f"=> put({chave!r}, {valor!r}) -> len={len(tabela)}")
    elif op == "get":
        resultado = tabela.get(chave)
        print(f"=> get({chave!r}) -> {resultado!r}")
    elif op == "delete":
        removido = tabela.delete(chave)
        print(f"=> delete({chave!r}) -> removido={removido}, len={len(tabela)}")


print("\n\n===== Teste 2 - Correctude após rehash =====\n")

tabela_rehash = HashTableChained(capacidade_inicial=7, limiar_carga=0.75)
n_inseridos = 50
dados_originais = {f"chave_{i}": i * 10 for i in range(n_inseridos)}

for chave, valor in dados_originais.items():
    tabela_rehash.put(chave, valor)

print(f"Elementos inseridos: {n_inseridos}")
print(f"Rehashes realizados: {tabela_rehash.total_rehashes}")
print(f"Capacidade final: {tabela_rehash.capacidade}")
print(f"Fator de carga: {tabela_rehash.fator_carga():.3f}")
print(f"len(tabela): {len(tabela_rehash)}\n")

falhas = 0
for chave, valor_esperado in dados_originais.items():
    resultado = tabela_rehash.get(chave)

    if resultado != valor_esperado:
        print(f"Falha: get({chave!r}) retornou {resultado!r}, esperado {valor_esperado!r}")
        falhas += 1

if falhas == 0:
    print(f"Todas as {n_inseridos} chaves acessíveis após {tabela_rehash.total_rehashes} rehash(es) ✅")
else:
    print(f"{falhas} chave(s) com falha após rehash ❌")


print("\n\n===== Teste 3 - Comparações por operação vs fator de carga =====\n")

limiares = [0.50, 0.75, 1.00, 2.00]
n_ops = 1000

print(f"{'limiar':>8}  {'capacidade':>12}  {'rehashes':>10}  {'comp_total':>12}  {'comp/op':>10}  {'carga_final':>12}")
print("-" * 74)

for limiar in limiares:
    t = HashTableChained(capacidade_inicial=11, limiar_carga=limiar)
    
    for i in range(n_ops):
        t.put(f"k{i}", i)

    comp_get = 0
    
    for i in range(n_ops):
        t.resetar_contadores()
        t.get(f"k{i}")
        comp_get += t.total_comparacoes

    comp_por_op = comp_get / n_ops
    print(f"{limiar:>8.2f}  {t.capacidade:>12}  {t.total_rehashes:>10}  {comp_get:>12}  {comp_por_op:>10.4f}  {t.fator_carga():>12.4f}")


print("\n\n===== Teste 4 - Distribuição dos elementos nos buckets =====\n")

t_dist = HashTableChained(capacidade_inicial=11, limiar_carga=10.0)
for i in range(50):
    t_dist.put(random.randint(0, 9999), i)

distribuicao = t_dist.distribuicao_buckets()
max_cadeia = max(distribuicao)
buckets_vazios = distribuicao.count(0)

print(f"Capacidade: {t_dist.capacidade}")
print(f"Elementos: {len(t_dist)}")
print(f"Fator de carga: {t_dist.fator_carga():.3f}")
print(f"Maior cadeia: {max_cadeia}")
print(f"Buckets vazios: {buckets_vazios}/{t_dist.capacidade}")
print(f"\nComprimento por bucket:")

for i, tamanho in enumerate(distribuicao):
    barra = "[]" * tamanho
    print(f"bucket[{i:>2}]: {tamanho:>2}  {barra}")
