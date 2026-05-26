from typing import List, Dict, Optional, Tuple
from collections import deque


class RedeSocial:
    """
    Rede social modelada como grafo não direcionado com vértices nomeados

    Attributes:
        _adjacencia (Dict[str, List[str]]): Mapa de cada pessoa para suas conexões diretas
    """

    def __init__(self) -> None:
        self._adjacencia: Dict[str, List[str]] = {}


    def adicionar_pessoa(self, pessoa: str) -> None:
        """
        Adiciona uma pessoa à rede caso ainda não exista

        Args:
            pessoa (str): Nome da pessoa a ser adicionada
        """

        if pessoa not in self._adjacencia:
            self._adjacencia[pessoa] = []


    def adicionar_conexao(self, a: str, b: str) -> None:
        """
        Adiciona uma conexão bidirecional entre duas pessoas

        Args:
            a (str): Primeira pessoa da conexão
            b (str): Segunda pessoa da conexão
        """

        self.adicionar_pessoa(a)
        self.adicionar_pessoa(b)
        self._adjacencia[a].append(b)
        self._adjacencia[b].append(a)


    def vizinhos(self, pessoa: str) -> List[str]:
        """
        Retorna as conexões diretas de uma pessoa

        Args:
            pessoa (str): Pessoa consultada

        Returns:
            List[str]: Lista de pessoas conectadas diretamente
        """

        return self._adjacencia[pessoa]


    def pessoas(self) -> List[str]:
        """
        Retorna todas as pessoas cadastradas na rede

        Returns:
            List[str]: Lista de pessoas
        """

        return list(self._adjacencia.keys())


    def num_pessoas(self) -> int:
        """
        Retorna o número total de pessoas na rede

        Returns:
            int: Número de pessoas
        """

        return len(self._adjacencia)


    def num_conexoes(self) -> int:
        """
        Retorna o número total de conexões na rede

        Returns:
            int: Número de conexões
        """

        return sum(len(v) for v in self._adjacencia.values()) // 2


    def __repr__(self) -> str:
        return f"RedeSocial(pessoas = {self.num_pessoas()}, conexoes = {self.num_conexoes()})"


def bfs_menor_caminho(rede: RedeSocial, origem: str, destino: str) -> Tuple[Optional[List[str]], int]:
    """
    Encontra o menor caminho entre duas pessoas usando BFS e reconstrói a sequência de vértices

    Args:
        rede (RedeSocial): Rede social a ser percorrida
        origem (str): Pessoa de partida
        destino (str): Pessoa de chegada

    Returns:
        Tuple[Optional[List[str]], int]: Par com a lista de pessoas no caminho mínimo e a distância em número de arestas, ou None e -1 se não houver caminho
    """

    if origem == destino:
        return [origem], 0

    predecessores: Dict[str, Optional[str]] = {origem: None}
    fila: deque = deque([origem])

    while fila:
        atual = fila.popleft()

        for vizinho in rede.vizinhos(atual):
            if vizinho not in predecessores:
                predecessores[vizinho] = atual
                fila.append(vizinho)

                if vizinho == destino:
                    return _reconstruir_caminho(predecessores, origem, destino)

    return None, -1


def _reconstruir_caminho(predecessores: Dict[str, Optional[str]], origem: str, destino: str) -> Tuple[List[str], int]:
    """
    Reconstrói o caminho mínimo a partir do mapa de predecessores gerado pela BFS

    Args:
        predecessores (Dict[str, Optional[str]]): Mapa de cada vértice para o vértice que o descobriu
        origem (str): Vértice de partida
        destino (str): Vértice de chegada

    Returns:
        Tuple[List[str], int]: Par com a lista de vértices no caminho e a distância em número de arestas
    """

    caminho: List[str] = []
    atual: Optional[str] = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    caminho.reverse()
    return caminho, len(caminho) - 1


def construir_rede_social() -> RedeSocial:
    """
    Constrói a rede social com as conexões definidas no enunciado

    Returns:
        RedeSocial: Rede social preenchida com todas as conexões
    """

    rede = RedeSocial()
    conexoes = [
        ("Idris", "Kamil"),
        ("Idris", "Talia"),
        ("Kamil", "Lina"),
        ("Lina", "Sasha"),
        ("Sasha", "Marco"),
        ("Marco", "Ken"),
        ("Ken", "Talia"),
    ]

    for a, b in conexoes:
        rede.adicionar_conexao(a, b)

    return rede


print("\n===== Teste 1 - Menor Caminho entre Idris e Lina =====\n")
rede = construir_rede_social()
print(f"Rede construída: {rede}\n")
caminho, distancia = bfs_menor_caminho(rede, "Idris", "Lina")
print(f"Caminho mínimo: {' -> '.join(caminho)}")
print(f"Distância: {distancia} conexão(ões)")


print("\n\n===== Teste 2 - Menor Caminho entre Todos os Pares da Rede =====\n")
pessoas = rede.pessoas()
print(f"{'Origem':<10}  {'Destino':<10}  {'Distância':<12}  {'Caminho'}")
print(f"{'-' * 10}  {'-' * 10}  {'-' * 12}  {'-' * 45}")

for i, origem in enumerate(pessoas):
    for destino in pessoas[i + 1:]:
        cam, dist = bfs_menor_caminho(rede, origem, destino)
        caminho_str = " -> ".join(cam) if cam else "sem caminho"
        print(f"{origem:<10}  {destino:<10}  {dist:<12}  {caminho_str}")


print("\n\n===== Teste 3 - Caminho entre Pessoas Sem Conexão Direta =====\n")
pares_indiretos = [("Idris", "Marco"), ("Talia", "Lina"), ("Kamil", "Ken")]

for origem, destino in pares_indiretos:
    cam, dist = bfs_menor_caminho(rede, origem, destino)
    print(f"{origem} -> {destino}")
    print(f"Caminho: {' -> '.join(cam)}")
    print(f"Distância: {dist} conexão(ões)\n")


print("\n===== Teste 4 - Caminho de uma Pessoa para Si Mesma =====\n")
cam, dist = bfs_menor_caminho(rede, "Idris", "Idris")
print(f"Caminho de Idris para Idris: {cam}")
print(f"Distância: {dist}")


print("\n\n===== Teste 5 - Caminho em Rede com Vértice Isolado =====\n")
rede_com_isolado = construir_rede_social()
rede_com_isolado.adicionar_pessoa("Nova")
cam, dist = bfs_menor_caminho(rede_com_isolado, "Idris", "Nova")
print(f"Caminho de Idris para Nova (isolada): {cam}")
print(f"Distância: {dist} (indica ausência de caminho)")


print("\n\n===== Teste 6 - Grau de Separação a Partir de Idris =====\n")
print(f"{'Pessoa':<10}  {'Grau de separação'}")
print(f"{'-' * 10}  {'-' * 18}")

for pessoa in pessoas:
    _, dist = bfs_menor_caminho(rede, "Idris", pessoa)
    grau = str(dist) if dist >= 0 else "sem conexao"
    print(f"{pessoa:<10}  {grau}")
print()
