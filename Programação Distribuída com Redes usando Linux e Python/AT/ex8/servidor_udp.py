import socket
import random
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 9001
TAMANHO_BUFFER = 1024
SEMENTE_ALEATORIA = 4


def criar_socket_servidor(host: str, porta: int) -> socket.socket:
    """
    Cria e configura o socket UDP do servidor pronto para receber mensagens

    Args:
        host (str): Endereço de escuta do servidor
        porta (int): Porta de escuta do servidor

    Returns:
        socket.socket: Socket UDP configurado e vinculado
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, porta))
    return sock


def enviar_com_perda(sock: socket.socket, ack: bytes, endereco: Tuple[str, int]) -> bool:
    """
    Envia o ACK ao cliente com probabilidade de 50% de descarte simulado

    Args:
        sock (socket.socket): Socket UDP do servidor
        ack (bytes): Bytes do ACK a enviar
        endereco (Tuple[str, int]): Endereço IP e porta do cliente

    Returns:
        bool: True se o ACK foi efetivamente enviado, False se foi descartado
    """

    if random.random() < 0.5:
        sock.sendto(ack, endereco)
        return True

    return False


def exibir_cabecalho() -> None:
    """
    Exibe o cabeçalho de identificação do servidor no terminal
    """

    print(f"\n{'=' * 60}")
    print("SERVIDOR UDP COM SIMULAÇÃO DE PERDA")
    print(f"{'=' * 60}\n")


def processar_mensagem(sock: socket.socket, dados: bytes, endereco: Tuple[str, int], numero: int) -> None:
    """
    Processa uma mensagem recebida, decide o envio do ACK e exibe o resultado

    Args:
        sock (socket.socket): Socket UDP do servidor
        dados (bytes): Bytes da mensagem recebida
        endereco (Tuple[str, int]): Endereço IP e porta do cliente
        numero (int): Contador sequencial da mensagem recebida
    """

    mensagem = dados.decode("utf-8", errors="replace")
    ack = b"ACK"
    enviado = enviar_com_perda(sock, ack, endereco)
    status_ack = "enviado" if enviado else "descartado"

    print(f"  Mensagem {numero}:")
    print(f"    Origem: {endereco[0]}:{endereco[1]}")
    print(f"    Conteúdo: {mensagem}")
    print(f"    ACK: {status_ack}\n")


def executar_servidor(host: str, porta: int) -> None:
    """
    Inicializa o servidor UDP e entra em loop recebendo mensagens indefinidamente

    Args:
        host (str): Endereço de escuta do servidor
        porta (int): Porta de escuta do servidor
    """

    random.seed(SEMENTE_ALEATORIA)
    sock = criar_socket_servidor(host, porta)
    exibir_cabecalho()
    print(f"  Aguardando mensagens em {host}:{porta}\n")

    contador = 1

    while True:
        dados, endereco = sock.recvfrom(TAMANHO_BUFFER)
        processar_mensagem(sock, dados, endereco, contador)
        contador += 1


executar_servidor(HOST, PORTA)
