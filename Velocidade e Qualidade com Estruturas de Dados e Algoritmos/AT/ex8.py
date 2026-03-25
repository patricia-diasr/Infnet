from typing import Any, List, Optional, Tuple, Dict
import math


class NoBucket:
    """
    Nó de uma lista encadeada que armazena um par (chave, valor)

    Attributes:
        chave: Chave de identificação do par (tupla (i, capacidade_restante))
        valor: Valor máximo calculado para este estado
        proximo (Optional[NoBucket]): Próximo nó na cadeia do bucket
    """

    def __init__(self, chave: Any, valor: Any) -> None:
        self.chave: Any = chave
        self.valor: Any = valor
        self.proximo: Optional["NoBucket"] = None


class HashTableMemo:
    """
    Hashtable com encadeamento usada como cache de memoization para o Knapsack

    Attributes:
        capacidade (int): Número atual de buckets
        total_elementos (int): Estados armazenados no cache
    """

    LIMIAR = 0.75
    CAP_INICIAL = 17

    def __init__(self) -> None:
        self.capacidade: int = self.CAP_INICIAL
        self.total_elementos: int = 0
        self._buckets: List[Optional[NoBucket]] = [None] * self.capacidade

    def put(self, chave: Any, valor: Any) -> None:
        """Insere ou atualiza um resultado no cache"""

        indice = hash(chave) % self.capacidade
        no = self._buckets[indice]

        while no:
            if no.chave == chave:
                no.valor = valor
                return
            no = no.proximo

        novo = NoBucket(chave, valor)
        novo.proximo = self._buckets[indice]
        self._buckets[indice] = novo
        self.total_elementos += 1

        if self.total_elementos / self.capacidade > self.LIMIAR:
            self._rehash()

    def get(self, chave: Any) -> Tuple[bool, Any]:
        """Recupera um resultado do cache se existir"""

        indice = hash(chave) % self.capacidade
        no = self._buckets[indice]

        while no:
            if no.chave == chave:
                return True, no.valor
            no = no.proximo
        
        return False, None

    def _rehash(self) -> None:
        nova_cap = self.capacidade * 2 + 1
        novos = [None] * nova_cap
        
        for bucket in self._buckets:
            no = bucket
            while no:
                idx = hash(no.chave) % nova_cap
                novo = NoBucket(no.chave, no.valor)
                novo.proximo = novos[idx]
                novos[idx] = novo
                no = no.proximo
        
        self._buckets = novos
        self.capacidade = nova_cap

    def __len__(self) -> int:
        return self.total_elementos


def knapsack_recursivo(pesos: List[int], valores: List[int], capacidade: int, n: int, _contadores: dict) -> int:
    """
    Solução recursiva pura para o Problema da Mochila 0/1

    Args:
        pesos (List[int]): Pesos dos itens disponíveis
        valores (List[int]): Valores dos itens disponíveis
        capacidade (int): Capacidade restante da mochila
        n (int): Índice do item atual sendo considerado
        _contadores (dict): Acumula 'chamadas' e 'distintos' (pares n, cap)

    Returns:
        int: Valor máximo total possível
    """
    _contadores["chamadas"] += 1
    _contadores["distintos"].add((n, capacidade))

    if n == 0 or capacidade == 0:
        return 0

    if pesos[n-1] > capacidade:
        return knapsack_recursivo(pesos, valores, capacidade, n-1, _contadores)

    incluir = valores[n-1] + knapsack_recursivo(pesos, valores, capacidade - pesos[n-1], n-1, _contadores)
    excluir = knapsack_recursivo(pesos, valores, capacidade, n-1, _contadores)

    return max(incluir, excluir)


def knapsack_memo(pesos: List[int], valores: List[int], capacidade: int, n: int, memo: HashTableMemo, _contadores: dict) -> int:
    """
    Solução do Problema da Mochila 0/1 com Memoization via HashTableMemo

    Args:
        pesos (List[int]): Pesos dos itens
        valores (List[int]): Valores dos itens
        capacidade (int): Capacidade restante
        n (int): Índice do item atual
        memo (HashTableMemo): Estrutura de cache
        _contadores (dict): Acumula 'chamadas' e 'distintos'

    Returns:
        int: Valor máximo total possível
    """

    _contadores["chamadas"] += 1
    chave = (n, capacidade)
    
    encontrado, valor_cached = memo.get(chave)
    if encontrado:
        return valor_cached

    _contadores["distintos"].add(chave)

    if n == 0 or capacidade == 0:
        resultado = 0

    elif pesos[n-1] > capacidade:
        resultado = knapsack_memo(pesos, valores, capacidade, n-1, memo, _contadores)

    else:
        incluir = valores[n-1] + knapsack_memo(pesos, valores, capacidade - pesos[n-1], n-1, memo, _contadores)
        excluir = knapsack_memo(pesos, valores, capacidade, n-1, memo, _contadores)
        resultado = max(incluir, excluir)

    memo.put(chave, resultado)
    return resultado


itens_valores = [60, 100, 120, 80, 30, 70, 45, 50, 90, 110, 150, 40, 200, 10, 25, 35]
itens_pesos   = [10, 20, 30, 15, 5, 12, 8, 10, 18, 22, 25, 9, 35, 3, 6, 7]
capacidade_max = 50

print("\n===== Teste 1 - Validação Recursivo vs Memoizado (Mochila 0/1) =====\n")

cont_rec = {"chamadas": 0, "distintos": set()}
res_rec = knapsack_recursivo(itens_pesos, itens_valores, capacidade_max, len(itens_valores), cont_rec)

memo = HashTableMemo()
cont_mem = {"chamadas": 0, "distintos": set()}
res_mem = knapsack_memo(itens_pesos, itens_valores, capacidade_max, len(itens_valores), memo, cont_mem)

print(f"Capacidade da Mochila: {capacidade_max}")
print(f"Itens disponíveis: {len(itens_valores)}")
print(f"Resultado Recursivo: {res_rec}")
print(f"Resultado Memoizado: {res_mem}")
print(f"Status: {'✅ Equivalentes' if res_rec == res_mem else '❌ Erro'}")


print("\n\n===== Teste 2 - Análise de Redução de Esforço =====\n")

print(f"{'Método':<16}  {'Chamadas':>12}  {'Subproblemas':>15}")
print("-" * 46)
print(f"{'Recursivo Puro':<16}  {cont_rec['chamadas']:>12}  {len(cont_rec['distintos']):>15}")
print(f"{'Memoizado':<16}  {cont_mem['chamadas']:>12}  {len(cont_mem['distintos']):>15}")

reducao = (1 - cont_mem["chamadas"] / cont_rec["chamadas"]) * 100
print(f"\nRedução de chamadas recursivas: {reducao:.2f}%")


print("\n\n===== Teste 3 - Escala de Complexidade =====\n")

print(f"{'Itens (n)':>8}  {'Rec Chamadas':>16}  {'Memo Chamadas':>16}  {'Ganho':>10}")
print("-" * 55)

for n_test in [4, 8, 12, 16]:
    v_t, p_t = itens_valores[:n_test], itens_pesos[:n_test]
    
    c_r = {"chamadas": 0, "distintos": set()}
    knapsack_recursivo(p_t, v_t, capacidade_max, n_test, c_r)
    
    m_t = HashTableMemo()
    c_m = {"chamadas": 0, "distintos": set()}
    knapsack_memo(p_t, v_t, capacidade_max, n_test, m_t, c_m)
    
    ganho = c_r['chamadas'] / c_m['chamadas']
    print(f"{n_test:>8}  {c_r['chamadas']:>16}  {c_m['chamadas']:>16}  {ganho:>9.1f}x")
    