import socket
import struct
import time
import random
from typing import Optional, List, Tuple


class ErroIPInvalido(Exception):
    """Levantada ao tentar processar um endereco IP com formato invalido"""


class ErroPreFixoInvalido(Exception):
    """Levantada ao tentar inserir um prefixo CIDR com formato invalido"""


class NodoTrie:
    """
    Nodo de uma Trie binaria para roteamento LPM

    Attributes:
        filhos (List[Optional[NodoTrie]]): Ponteiros para os filhos, indice 0 para bit 0 e indice 1 para bit 1
        rota_id (Optional[int]): Identificador da rota se este nodo for terminal, None caso contrario
        is_terminal (bool): Indica se este nodo representa o fim de um prefixo cadastrado
    """

    __slots__ = ("filhos", "rota_id", "is_terminal")

    def __init__(self) -> None:
        self.filhos: List[Optional["NodoTrie"]] = [None, None]
        self.rota_id: Optional[int] = None
        self.is_terminal: bool = False


    def __repr__(self) -> str:
        return f"NodoTrie(terminal={self.is_terminal}, rota_id={self.rota_id})"


def _ip4_para_int(ip: str) -> int:
    """
    Converte um endereco IPv4 em um inteiro de 32 bits

    Args:
        ip (str): Endereco IPv4 no formato dotted-decimal (ex: 192.168.1.1)

    Returns:
        int: Representacao inteira de 32 bits do endereco

    Raises:
        ErroIPInvalido: Se o formato do endereco for invalido
    """

    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]

    except (socket.error, struct.error):
        raise ErroIPInvalido(f"Endereco IPv4 invalido: '{ip}'")


def _ip6_para_int(ip: str) -> int:
    """
    Converte um endereco IPv6 em um inteiro de 128 bits

    Args:
        ip (str): Endereco IPv6 no formato padrao (ex: 2001:db8::1)

    Returns:
        int: Representacao inteira de 128 bits do endereco

    Raises:
        ErroIPInvalido: Se o formato do endereco for invalido
    """

    try:
        raw = socket.inet_pton(socket.AF_INET6, ip)
        alto, baixo = struct.unpack("!QQ", raw)
        return (alto << 64) | baixo

    except (socket.error, struct.error):
        raise ErroIPInvalido(f"Endereco IPv6 invalido: '{ip}'")


def _detectar_versao(ip: str) -> int:
    """
    Detecta se um endereco IP e da versao 4 ou 6

    Args:
        ip (str): Endereco IP a ser analisado

    Returns:
        int: 4 para IPv4 ou 6 para IPv6

    Raises:
        ErroIPInvalido: Se o formato nao for reconhecido como IPv4 nem IPv6
    """

    if ":" in ip:
        return 6

    if "." in ip:
        return 4

    raise ErroIPInvalido(f"Formato de endereco nao reconhecido: '{ip}'")


def _parsear_cidr(prefixo: str) -> Tuple[int, int, int]:
    """
    Faz o parse de um prefixo CIDR retornando o inteiro do IP, o comprimento e a versao

    Args:
        prefixo (str): Prefixo no formato CIDR (ex: 192.168.1.0/24 ou 2001:db8::/32)

    Returns:
        Tuple[int, int, int]: Tupla (ip_int, comprimento, versao) onde versao e 4 ou 6

    Raises:
        ErroPreFixoInvalido: Se o formato CIDR for invalido
    """

    try:
        ip_str, comprimento_str = prefixo.split("/")
        comprimento = int(comprimento_str)

    except ValueError:
        raise ErroPreFixoInvalido(f"Prefixo CIDR invalido: '{prefixo}'")

    versao = _detectar_versao(ip_str)
    bits_totais = 32 if versao == 4 else 128

    if not (0 <= comprimento <= bits_totais):
        raise ErroPreFixoInvalido(f"Comprimento de prefixo {comprimento} fora do intervalo para IPv{versao}")

    ip_int = _ip4_para_int(ip_str) if versao == 4 else _ip6_para_int(ip_str)
    return ip_int, comprimento, versao


def _extrair_bit(ip_int: int, posicao: int, bits_totais: int) -> int:
    """
    Extrai o bit em uma posicao especifica de um inteiro representando um IP

    Args:
        ip_int (int): Endereco IP representado como inteiro
        posicao (int): Posicao do bit, onde 0 e o bit mais significativo
        bits_totais (int): Total de bits do endereco (32 para IPv4, 128 para IPv6)

    Returns:
        int: Valor do bit (0 ou 1)
    """

    return (ip_int >> (bits_totais - 1 - posicao)) & 1


class PoolNodos:
    """
    Pool de nodos pre-alocados para reducao de fragmentacao de memoria e cache misses

    Attributes:
        _bloco (List[NodoTrie]): Lista contigua de nodos pre-alocados
        _proximo (int): Indice do proximo nodo livre no pool
    """

    def __init__(self, capacidade: int) -> None:
        self._bloco: List[NodoTrie] = [NodoTrie() for _ in range(capacidade)]
        self._proximo: int = 0


    def alocar(self) -> NodoTrie:
        """
        Retorna o proximo nodo livre do pool, expandindo se necessario

        Returns:
            NodoTrie: Nodo disponivel para uso
        """

        if self._proximo >= len(self._bloco):
            self._bloco.extend(NodoTrie() for _ in range(len(self._bloco)))

        nodo = self._bloco[self._proximo]
        nodo.filhos = [None, None]
        nodo.rota_id = None
        nodo.is_terminal = False
        self._proximo += 1
        return nodo


    def total_alocados(self) -> int:
        """
        Retorna o numero de nodos efetivamente alocados

        Returns:
            int: Total de nodos em uso
        """

        return self._proximo


class TrieBinaria:
    """
    Trie binaria para busca de prefixo mais longo (LPM) com suporte a IPv4 e IPv6

    Attributes:
        _pool (PoolNodos): Pool contiguo de nodos para reduzir cache misses
        _raiz_v4 (NodoTrie): Nodo raiz da trie IPv4
        _raiz_v6 (NodoTrie): Nodo raiz da trie IPv6
        _total_rotas (int): Numero total de rotas inseridas
    """

    def __init__(self, capacidade_inicial: int = 1024) -> None:
        self._pool: PoolNodos = PoolNodos(capacidade_inicial)
        self._raiz_v4: NodoTrie = self._pool.alocar()
        self._raiz_v6: NodoTrie = self._pool.alocar()
        self._total_rotas: int = 0


    def _raiz_para_versao(self, versao: int) -> NodoTrie:
        """
        Retorna a raiz correspondente a versao do protocolo IP

        Args:
            versao (int): Versao do protocolo (4 ou 6)

        Returns:
            NodoTrie: Nodo raiz da trie correspondente
        """

        return self._raiz_v4 if versao == 4 else self._raiz_v6


    def inserir(self, prefixo: str, rota_id: int) -> None:
        """
        Insere um prefixo CIDR na trie associando-o a um identificador de rota

        Args:
            prefixo (str): Prefixo no formato CIDR (ex: 10.0.0.0/8)
            rota_id (int): Identificador numerico da rota a ser associada

        Raises:
            ErroPreFixoInvalido: Se o prefixo CIDR tiver formato invalido
        """

        ip_int, comprimento, versao = _parsear_cidr(prefixo)
        bits_totais = 32 if versao == 4 else 128
        nodo_atual = self._raiz_para_versao(versao)

        for posicao in range(comprimento):
            bit = _extrair_bit(ip_int, posicao, bits_totais)

            if nodo_atual.filhos[bit] is None:
                nodo_atual.filhos[bit] = self._pool.alocar()
            
            nodo_atual = nodo_atual.filhos[bit]

        if not nodo_atual.is_terminal:
            self._total_rotas += 1

        nodo_atual.is_terminal = True
        nodo_atual.rota_id = rota_id


    def lookup(self, ip: str) -> Optional[int]:
        """
        Realiza a busca pelo prefixo mais longo que coincide com o IP informado

        Args:
            ip (str): Endereco IP a ser roteado (IPv4 ou IPv6)

        Returns:
            Optional[int]: Identificador da rota mais especifica encontrada, ou None se nenhuma

        Raises:
            ErroIPInvalido: Se o formato do endereco for invalido
        """

        versao = _detectar_versao(ip)
        bits_totais = 32 if versao == 4 else 128
        ip_int = _ip4_para_int(ip) if versao == 4 else _ip6_para_int(ip)

        nodo_atual = self._raiz_para_versao(versao)
        ultima_rota: Optional[int] = None

        if nodo_atual.is_terminal:
            ultima_rota = nodo_atual.rota_id

        for posicao in range(bits_totais):
            bit = _extrair_bit(ip_int, posicao, bits_totais)
            proximo = nodo_atual.filhos[bit]

            if proximo is None:
                break

            nodo_atual = proximo

            if nodo_atual.is_terminal:
                ultima_rota = nodo_atual.rota_id

        return ultima_rota


    def total_rotas(self) -> int:
        """
        Retorna o numero total de rotas cadastradas na trie

        Returns:
            int: Numero de rotas
        """

        return self._total_rotas


    def __repr__(self) -> str:
        return (f"TrieBinaria(rotas={self._total_rotas}, nodos_alocados={self._pool.total_alocados()}, capacidade_pool={len(self._pool._bloco)})")


class Roteador:
    """
    Roteador de alta performance baseado em Trie binaria com suporte a IPv4 e IPv6

    Attributes:
        _trie (TrieBinaria): Estrutura de busca de prefixo mais longo
        _mapa_rotas (dict): Mapa de rota_id para descricao textual da rota
    """

    def __init__(self) -> None:
        self._trie: TrieBinaria = TrieBinaria()
        self._mapa_rotas: dict = {}


    def adicionar_rota(self, prefixo: str, rota_id: int, descricao: str = "") -> None:
        """
        Adiciona uma rota a tabela de roteamento

        Args:
            prefixo (str): Prefixo CIDR da rota (ex: 192.168.1.0/24)
            rota_id (int): Identificador numerico unico da rota
            descricao (str): Descricao textual opcional da rota

        Raises:
            ErroPreFixoInvalido: Se o prefixo CIDR for invalido
        """

        self._trie.inserir(prefixo, rota_id)
        self._mapa_rotas[rota_id] = descricao or prefixo


    def rotear(self, ip: str) -> Tuple[Optional[int], str]:
        """
        Determina a rota mais especifica para um endereco IP de destino

        Args:
            ip (str): Endereco IP de destino (IPv4 ou IPv6)

        Returns:
            Tuple[Optional[int], str]: Par (rota_id, descricao) da rota encontrada, ou (None, 'sem rota') se nenhuma

        Raises:
            ErroIPInvalido: Se o formato do endereco IP for invalido
        """

        rota_id = self._trie.lookup(ip)

        if rota_id is None:
            return None, "sem rota"

        return rota_id, self._mapa_rotas.get(rota_id, "rota desconhecida")


    def total_rotas(self) -> int:
        """
        Retorna o numero de rotas cadastradas no roteador

        Returns:
            int: Total de rotas
        """

        return self._trie.total_rotas()


    def __repr__(self) -> str:
        return f"Roteador(rotas={self.total_rotas()}, trie={self._trie})"



roteador = Roteador()
tabela = [
    ("0.0.0.0/0", 50, "Default Gateway (rota padrao)"),
    ("10.0.0.0/8", 40, "Rede de grande porte 10.x.x.x"),
    ("192.168.0.0/16", 10, "Rota generica para rede local"),
    ("192.168.1.0/24", 20, "Sub-rede especifica 1"),
    ("192.168.1.128/25", 30, "Sub-rede ainda mais especifica"),
    ("2001:db8::/32", 100, "Prefixo IPv6 generico"),
    ("2001:db8:a::/48", 200, "Sub-rede IPv6 especifica"),
]

for prefixo, rota_id, descricao in tabela:
    roteador.adicionar_rota(prefixo, rota_id, descricao)


print("\n===== Tabela de Roteamento Cadastrada =====\n")
print(f"{'Prefixo':<22}  {'ID':>4}  {'Descricao'}")
print(f"{'-'*22}  {'-'*4}  {'-'*35}")
for prefixo, rota_id, descricao in tabela:
    print(f"{prefixo:<22}  {rota_id:>4}  {descricao}")
print(f"\nTotal de rotas: {roteador.total_rotas()}")
print(f"Representacao : {roteador}\n")


print("\n===== Teste 1 - Casos de Lookup =====\n")
casos = [
    ("192.168.0.50", 10, "Coincide apenas com /16"),
    ("192.168.1.20", 20, "Coincide com /16 e /24, vence o /24"),
    ("192.168.1.150", 30, "Coincide com /16, /24 e /25, vence o /25"),
    ("10.255.0.1", 40, "Coincide com 10.0.0.0/8"),
    ("8.8.8.8", 50, "Nenhuma rota especifica, cai na 0.0.0.0/0"),
    ("2001:db8:cafe::1", 100, "Coincide com o prefixo /32"),
    ("2001:db8:a:b::1", 200, "Coincide com /48, mais especifico que /32"),
]

print(f"{'IP de Destino':<22}  {'Esperado':>8}  {'Obtido':>8}  {'Status':<6}  {'Motivo'}")
print(f"{'-'*22}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*40}")

acertos = 0
for ip, esperado, motivo in casos:
    obtido, descricao = roteador.rotear(ip)
    status = "OK" if obtido == esperado else "FALHA"
    if status == "OK":
        acertos += 1
    print(f"{ip:<22}  {esperado:>8}  {str(obtido):>8}  {status:<6}  {motivo}")

print(f"\nResultado: {acertos}/{len(casos)} casos corretos\n")


print("\n===== Teste 2 - Casos de Borda =====\n")
borda = [
    ("0.0.0.0", 50, "Proprio default gateway"),
    ("10.0.0.0", 40, "Inicio exato da rede /8"),
    ("10.255.255.255", 40, "Fim da rede /8"),
    ("192.168.1.128", 30, "Inicio exato da sub-rede /25"),
    ("192.168.1.255", 30, "Fim da sub-rede /25"),
    ("192.168.1.127", 20, "Ultimo IP antes da sub-rede /25, cai no /24"),
    ("172.16.0.1", 50, "Fora de qualquer rota especifica, cai no gateway"),
]
print(f"{'IP de Destino':<22}  {'Esperado':>8}  {'Obtido':>8}  {'Status':<6}  {'Motivo'}")
print(f"{'-'*22}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*42}")

acertos_borda = 0
for ip, esperado, borda_motivo in borda:
    obtido, _ = roteador.rotear(ip)
    status = "OK" if obtido == esperado else "FALHA"
    if status == "OK":
        acertos_borda += 1
    print(f"{ip:<22}  {esperado:>8}  {str(obtido):>8}  {status:<6}  {borda_motivo}")

print(f"\nResultado: {acertos_borda}/{len(borda)} casos corretos\n")


print("\n===== Teste 3 - Desempenho do Pool de Nodos =====\n")
roteador_perf = Roteador()
roteador_perf.adicionar_rota("0.0.0.0/0", 1, "gateway")
roteador_perf.adicionar_rota("10.0.0.0/8", 2, "rede corporativa")
roteador_perf.adicionar_rota("192.168.0.0/16", 3, "rede local")
roteador_perf.adicionar_rota("192.168.1.0/24", 4, "sub-rede 1")
roteador_perf.adicionar_rota("192.168.1.128/25", 5, "sub-rede especifica")

ips_teste = [
    f"{random.randint(0,255)}.{random.randint(0,255)}"
    f".{random.randint(0,255)}.{random.randint(0,255)}"
    for _ in range(10_000)
]

inicio = time.perf_counter()
for ip in ips_teste:
    roteador_perf.rotear(ip)
tempo_total = time.perf_counter() - inicio

print(f"Lookups realizados: 10.000")
print(f"Tempo total: {tempo_total * 1000:.3f} ms")
print(f"Media por lookup: {tempo_total / 10_000 * 1_000_000:.2f} us")
print(f"Throughput: {10_000 / tempo_total:,.0f} lookups/s\n")


print("\n===== Teste 4 - Verificacao da Trie sem Rota Padrao =====\n")
roteador_sem_padrao = Roteador()
roteador_sem_padrao.adicionar_rota("192.168.1.0/24", 99, "unica rota")

resultado, desc = roteador_sem_padrao.rotear("10.0.0.1")
print(f"IP sem rota correspondente -> ID obtido: {resultado}, descricao: '{desc}'")

resultado, desc = roteador_sem_padrao.rotear("192.168.1.100")
print(f"IP com rota correspondente -> ID obtido: {resultado}, descricao: '{desc}'\n")
