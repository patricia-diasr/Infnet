from typing import List, Dict, Tuple
from collections import deque


class RedeTuneis:
    """
    Rede de túneis modelada como grafo não direcionado com vértices indexados a partir de 1

    Attributes:
        _num_saloes (int): Número total de salões na rede
        _adjacencia (Dict[int, List[int]]): Mapa de cada salão para seus salões vizinhos
    """

    def __init__(self, num_saloes: int) -> None:
        self._num_saloes: int = num_saloes
        self._adjacencia: Dict[int, List[int]] = {i: [] for i in range(1, num_saloes + 1)}


    def adicionar_tunel(self, x: int, y: int) -> None:
        """
        Adiciona um túnel bidirecional entre dois salões

        Args:
            x (int): Primeiro salão do túnel
            y (int): Segundo salão do túnel
        """

        self._adjacencia[x].append(y)
        self._adjacencia[y].append(x)


    def vizinhos(self, salao: int) -> List[int]:
        """
        Retorna os salões diretamente conectados a um salão

        Args:
            salao (int): Salão consultado

        Returns:
            List[int]: Lista de salões adjacentes
        """

        return self._adjacencia[salao]


    def num_saloes(self) -> int:
        """
        Retorna o número total de salões da rede

        Returns:
            int: Número de salões
        """

        return self._num_saloes


    def __repr__(self) -> str:
        total_tuneis = sum(len(v) for v in self._adjacencia.values()) // 2
        return f"RedeTuneis(saloes = {self._num_saloes}, tuneis = {total_tuneis})"


def _bfs_conectados(rede: RedeTuneis, origem: int, destino: int) -> bool:
    """
    Verifica se existe algum caminho entre dois salões usando BFS

    Args:
        rede (RedeTuneis): Rede de túneis a ser percorrida
        origem (int): Salão de partida
        destino (int): Salão de chegada

    Returns:
        bool: True se existe caminho entre origem e destino, False caso contrário
    """

    if origem == destino:
        return True

    visitados: Dict[int, bool] = {origem: True}
    fila: deque = deque([origem])

    while fila:
        atual = fila.popleft()

        for vizinho in rede.vizinhos(atual):
            if vizinho == destino:
                return True

            if vizinho not in visitados:
                visitados[vizinho] = True
                fila.append(vizinho)

    return False


def _passeio_valido(rede: RedeTuneis, sequencia: List[int]) -> bool:
    """
    Verifica se um passeio é válido checando conectividade entre cada par consecutivo de salões

    Args:
        rede (RedeTuneis): Rede de túneis a ser consultada
        sequencia (List[int]): Sequência ordenada de salões do passeio

    Returns:
        bool: True se todos os pares consecutivos estão conectados, False caso contrário
    """

    for i in range(len(sequencia) - 1):
        origem = sequencia[i]
        destino = sequencia[i + 1]

        if not _bfs_conectados(rede, origem, destino):
            return False

    return True


def contar_passeios_validos(s: int, tuneis: List[Tuple[int, int]], passeios: List[List[int]]) -> int:
    """
    Constrói a rede de túneis e conta quantos passeios sugeridos são possíveis

    Args:
        s (int): Número de salões da rede
        tuneis (List[Tuple[int, int]]): Lista de pares (x, y) representando conexões entre salões
        passeios (List[List[int]]): Lista de sequências de salões representando sugestões de passeio

    Returns:
        int: Número de sugestões de passeio possíveis
    """

    rede = RedeTuneis(s)

    for x, y in tuneis:
        rede.adicionar_tunel(x, y)

    validos = 0

    for sequencia in passeios:
        if _passeio_valido(rede, sequencia):
            validos += 1

    return validos


print("\n===== Teste 1 - Caso com Passeios Válidos e Inválidos =====\n")
s1 = 5
tuneis1 = [(1, 2), (2, 3), (3, 4)]
passeios1 = [[1, 2, 3], [1, 4], [1, 5], [2, 4, 1]]
resultado1 = contar_passeios_validos(s1, tuneis1, passeios1)
print(f"Salões: {s1}")
print(f"Túneis: {tuneis1}")
print(f"{'Passeio':<25}  {'Válido'}")
print(f"{'-' * 25}  {'-' * 6}")
rede_t1 = RedeTuneis(s1)

for x, y in tuneis1:
    rede_t1.adicionar_tunel(x, y)

for seq in passeios1:
    valido = _passeio_valido(rede_t1, seq)
    print(f"{str(seq):<25}  {valido}")

print(f"\nTotal de passeios válidos: {resultado1}")
print(f"Esperado: 3 (passeio [1,5] inválido pois salão 5 está isolado)")


print("\n\n===== Teste 2 - Rede Totalmente Conectada =====\n")
s2 = 4
tuneis2 = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
passeios2 = [[1, 4], [2, 3, 1], [4, 2, 3, 1]]
resultado2 = contar_passeios_validos(s2, tuneis2, passeios2)
print(f"Salões: {s2}")
print(f"Túneis: {tuneis2}")
print(f"Total de passeios válidos: {resultado2}")
print(f"Esperado: 3 (todos válidos pois a rede é completamente conectada)")


print("\n\n===== Teste 3 - Rede Sem Túneis =====\n")
s3 = 3
tuneis3 = []
passeios3 = [[1, 2], [1], [2, 3]]
resultado3 = contar_passeios_validos(s3, tuneis3, passeios3)
print(f"Salões: {s3}")
print(f"Túneis: {tuneis3}")
print(f"Total de passeios válidos: {resultado3}")
print(f"Esperado: 1 (apenas o passeio com um único salão é válido)")


print("\n\n===== Teste 4 - Passeio com Salão Repetido =====\n")
s4 = 3
tuneis4 = [(1, 2), (2, 3)]
passeios4 = [[1, 2, 1, 3], [3, 1]]
resultado4 = contar_passeios_validos(s4, tuneis4, passeios4)
print(f"Salões: {s4}")
print(f"Túneis: {tuneis4}")
print(f"Total de passeios válidos: {resultado4}")
print(f"Esperado: 2 (revisitar salões é permitido pois basta haver caminho)")


print("\n\n===== Teste 5 - Duas Componentes Isoladas =====\n")
s5 = 6
tuneis5 = [(1, 2), (2, 3), (4, 5), (5, 6)]
passeios5 = [[1, 3], [4, 6], [1, 4], [2, 5]]
resultado5 = contar_passeios_validos(s5, tuneis5, passeios5)
print(f"Salões: {s5}")
print(f"Túneis: {tuneis5}")
print(f"{'Passeio':<15}  {'Válido'}")
print(f"{'-' * 15}  {'-' * 6}")
rede_t5 = RedeTuneis(s5)

for x, y in tuneis5:
    rede_t5.adicionar_tunel(x, y)

for seq in passeios5:
    valido = _passeio_valido(rede_t5, seq)
    print(f"{str(seq):<15}  {valido}")

print(f"\nTotal de passeios válidos: {resultado5}")
print(f"Esperado: 2 (passeios entre componentes distintas são inválidos)")


print("\n\n===== Teste 6 - Representação da Rede =====\n")
rede_exemplo = RedeTuneis(s5)
for x, y in tuneis5:
    rede_exemplo.adicionar_tunel(x, y)
print(f"Representação: {rede_exemplo}\n")
