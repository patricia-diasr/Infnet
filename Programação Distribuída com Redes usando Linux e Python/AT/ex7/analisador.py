import struct
from typing import Optional, Tuple
from scapy.all import sniff, TCP, Raw, Packet


PORTA_APLICACAO = 9000
TAMANHO_CABECALHO = 4
INTERFACE = "enp0s3"


def extrair_framing(payload: bytes) -> Optional[Tuple[int, int, bool]]:
    """
    Tenta interpretar o payload TCP como uma mensagem do protocolo de framing tamanho mais conteúdo

    Args:
        payload (bytes): Bytes brutos do payload TCP capturado

    Returns:
        Optional[Tuple[int, int, bool]]: (tamanho declarado, tamanho do conteúdo recebido, tem inconsistência)
        Retorna None se o payload for menor que o cabeçalho esperado
    """

    if len(payload) < TAMANHO_CABECALHO:
        return None

    tamanho_declarado = struct.unpack("!I", payload[:TAMANHO_CABECALHO])[0]
    tamanho_recebido = len(payload) - TAMANHO_CABECALHO
    inconsistente = tamanho_declarado != tamanho_recebido

    return tamanho_declarado, tamanho_recebido, inconsistente


def classificar_direcao(pacote: Packet) -> str:
    """
    Classifica a direção do pacote TCP em relação ao servidor da aplicação

    Args:
        pacote (Packet): Pacote TCP capturado pelo Scapy

    Returns:
        str: "cliente para servidor" ou "servidor para cliente"
    """

    if pacote[TCP].dport == PORTA_APLICACAO:
        return "cliente para servidor"

    return "servidor para cliente"


def processar_pacote(pacote: Packet) -> None:
    """
    Analisa um pacote TCP capturado e exibe as informações de framing identificadas

    Args:
        pacote (Packet): Pacote TCP capturado pelo Scapy
    """

    if not pacote.haslayer(TCP) or not pacote.haslayer(Raw):
        return

    tcp = pacote[TCP]

    if tcp.dport != PORTA_APLICACAO and tcp.sport != PORTA_APLICACAO:
        return

    payload = bytes(pacote[Raw].load)
    direcao = classificar_direcao(pacote)
    resultado = extrair_framing(payload)

    print(f"\n  Pacote capturado:")
    print(f"    Origem: {pacote.src}:{tcp.sport}")
    print(f"    Destino: {pacote.dst}:{tcp.dport}")
    print(f"    Direção: {direcao}")
    print(f"    Payload total: {len(payload)} bytes")

    if resultado is None:
        print(f"    Framing: payload insuficiente para leitura do cabeçalho")
        return

    tamanho_declarado, tamanho_recebido, inconsistente = resultado

    print(f"    Tamanho declarado: {tamanho_declarado} bytes")
    print(f"    Tamanho recebido: {tamanho_recebido} bytes")

    if inconsistente:
        diferenca = tamanho_declarado - tamanho_recebido
        print(f"    Inconsistência: Sim (diferença de {diferenca} bytes)")

    else:
        print(f"    Inconsistência: Não")


def executar_analisador(interface: str, porta: int) -> None:
    """
    Inicia a captura de pacotes TCP na interface e porta especificadas

    Args:
        interface (str): Nome da interface de rede a monitorar
        porta (int): Porta TCP da aplicação a filtrar
    """

    filtro = f"tcp port {porta}"

    print(f"\n{'=' * 60}")
    print("ANALISADOR DE TRÁFEGO TCP COM FRAMING")
    print(f"{'=' * 60}")
    print(f"\n  Interface: {interface}")
    print(f"  Filtro BPF: {filtro}")
    print(f"  Aguardando pacotes...\n")

    sniff(iface=interface, filter=filtro, prn=processar_pacote, store=False)


executar_analisador(INTERFACE, PORTA_APLICACAO)
