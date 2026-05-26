from typing import List, Dict, Tuple
from collections import deque


class RedeIlhas:
    """
    Rede de ilhas modelada como grafo não direcionado dinâmico com vértices indexados a partir de 1

    Attributes:
        _num_ilhas (int): Número total de ilhas na rede
        _adjacencia (Dict[int, List[int]]): Mapa de cada ilha para suas ilhas vizinhas
        _num_pontes (int): Número de pontes construídas até o momento
    """

    def __init__(self, num_ilhas: int) -> None:
        self._num_ilhas: int = num_ilhas
        self._adjacencia: Dict[int, List[int]] = {i: [] for i in range(1, num_ilhas + 1)}
        self._num_pontes: int = 0


    def construir_ponte(self, a: int, b: int) -> None:
        """
        Constrói uma ponte bidirecional entre duas ilhas

        Args:
            a (int): Primeira ilha da ponte
            b (int): Segunda ilha da ponte
        """

        self._adjacencia[a].append(b)
        self._adjacencia[b].append(a)
        self._num_pontes += 1


    def vizinhos(self, ilha: int) -> List[int]:
        """
        Retorna as ilhas diretamente conectadas a uma ilha

        Args:
            ilha (int): Ilha consultada

        Returns:
            List[int]: Lista de ilhas adjacentes
        """

        return self._adjacencia[ilha]


    def num_ilhas(self) -> int:
        """
        Retorna o número total de ilhas da rede

        Returns:
            int: Número de ilhas
        """

        return self._num_ilhas


    def num_pontes(self) -> int:
        """
        Retorna o número de pontes construídas até o momento

        Returns:
            int: Número de pontes
        """

        return self._num_pontes


    def __repr__(self) -> str:
        return f"RedeIlhas(ilhas = {self._num_ilhas}, pontes = {self._num_pontes})"


def _bfs_conectadas(rede: RedeIlhas, origem: int, destino: int) -> bool:
    """
    Verifica se existe algum caminho entre duas ilhas usando BFS

    Args:
        rede (RedeIlhas): Rede de ilhas a ser percorrida
        origem (int): Ilha de partida
        destino (int): Ilha de chegada

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


def processar_operacoes(n: int, operacoes: List[Tuple[int, int, int]]) -> List[int]:
    """
    Constrói a rede de ilhas e processa operações de construção de pontes e consultas de conectividade

    Args:
        n (int): Número de ilhas da rede
        operacoes (List[Tuple[int, int, int]]): Lista de operações no formato (tipo, a, b), onde tipo 1 constrói uma ponte e tipo 0 consulta conectividade entre a e b

    Returns:
        List[int]: Lista de respostas para cada consulta, sendo 1 se conectadas e 0 caso contrário
    """

    rede = RedeIlhas(n)
    respostas: List[int] = []

    for tipo, a, b in operacoes:
        if tipo == 1:
            rede.construir_ponte(a, b)

        else:
            conectadas = _bfs_conectadas(rede, a, b)
            respostas.append(1 if conectadas else 0)

    return respostas


print("\n===== Teste 1 - Caso com Construção e Consultas Intercaladas =====\n")
n1 = 4
operacoes1 = [(0, 1, 2), (1, 1, 2), (0, 1, 2), (1, 2, 3), (0, 1, 3), (0, 1, 4)]
respostas1 = processar_operacoes(n1, operacoes1)
print(f"Ilhas: {n1}")
print(f"{'Operação':<12}  {'Resposta'}")
print(f"{'-' * 12}  {'-' * 8}")

for (tipo, a, b), resp in zip([op for op in operacoes1 if op[0] == 0], respostas1):
    print(f"consulta {a}-{b}  {resp}")

print(f"\nRespostas: {respostas1}")
print(f"Esperado: [0, 1, 1, 0]")


print("\n\n===== Teste 2 - Todas as Consultas Antes de Qualquer Ponte =====\n")
n2 = 3
operacoes2 = [(0, 1, 2), (0, 2, 3), (0, 1, 3)]
respostas2 = processar_operacoes(n2, operacoes2)
print(f"Ilhas: {n2}")
print(f"Respostas: {respostas2}")
print(f"Esperado: [0, 0, 0] (nenhuma ponte construída ainda)")


print("\n\n===== Teste 3 - Conectividade Transitiva Formada Gradualmente =====\n")
n3 = 5
operacoes3 = [(1, 1, 2), (0, 1, 3), (1, 2, 3), (0, 1, 3), (1, 3, 4), (0, 1, 4), (0, 1, 5)]
respostas3 = processar_operacoes(n3, operacoes3)
print(f"Ilhas: {n3}")
print(f"{'Operação':<15}  {'Resposta'}")
print(f"{'-' * 15}  {'-' * 8}")
idx = 0

for tipo, a, b in operacoes3:
    if tipo == 1:
        print(f"ponte {a}-{b}        ")

    else:
        print(f"consulta {a}-{b}      {respostas3[idx]}")
        idx += 1

print(f"\nRespostas: {respostas3}")
print(f"Esperado: [0, 1, 1, 0]")


print("\n\n===== Teste 4 - Consulta entre a Mesma Ilha =====\n")
n4 = 3
operacoes4 = [(0, 2, 2), (0, 1, 1)]
respostas4 = processar_operacoes(n4, operacoes4)
print(f"Ilhas: {n4}")
print(f"Respostas: {respostas4}")
print(f"Esperado: [1, 1] (ilha sempre conectada a si mesma)")


print("\n\n===== Teste 5 - Múltiplas Pontes Redundantes =====\n")
n5 = 3
operacoes5 = [(1, 1, 2), (1, 1, 2), (1, 2, 3), (0, 1, 3), (0, 2, 3)]
respostas5 = processar_operacoes(n5, operacoes5)
print(f"Ilhas: {n5}")
print(f"Respostas: {respostas5}")
print(f"Esperado: [1, 1] (pontes duplicadas não quebram a conectividade)")


print("\n\n===== Teste 6 - Estado da Rede ao Final das Operações =====\n")
rede_final = RedeIlhas(n1)

for tipo, a, b in operacoes1:
    if tipo == 1:
        rede_final.construir_ponte(a, b)

print(f"Representação: {rede_final}\n")
