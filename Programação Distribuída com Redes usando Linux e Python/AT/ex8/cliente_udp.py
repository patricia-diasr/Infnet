import socket
from typing import List, Tuple


HOST_SERVIDOR = "192.168.56.101"
PORTA = 9001
TIMEOUT_SEGUNDOS = 2.0
MAX_TENTATIVAS = 5
TAMANHO_BUFFER = 1024


def criar_socket_cliente(timeout: float) -> socket.socket:
    """
    Cria e configura o socket UDP do cliente com timeout definido

    Args:
        timeout (float): Tempo máximo de espera em segundos por uma resposta

    Returns:
        socket.socket: Socket UDP configurado com timeout
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    return sock


def tentar_envio(sock: socket.socket, mensagem: bytes, endereco: Tuple[str, int], numero_tentativa: int) -> bool:
    """
    Realiza uma tentativa de envio da mensagem e aguarda o ACK dentro do timeout

    Args:
        sock (socket.socket): Socket UDP do cliente
        mensagem (bytes): Bytes da mensagem a enviar
        endereco (Tuple[str, int]): Endereço IP e porta do servidor
        numero_tentativa (int): Número sequencial da tentativa atual

    Returns:
        bool: True se o ACK foi recebido com sucesso, False em caso de timeout
    """

    sock.sendto(mensagem, endereco)
    print(f"  Tentativa {numero_tentativa}: mensagem enviada, aguardando ACK...")

    try:
        resposta, _ = sock.recvfrom(TAMANHO_BUFFER)
        ack = resposta.decode("utf-8", errors="replace")
        print(f"  Tentativa {numero_tentativa}: ACK recebido ({ack})")
        return True

    except socket.timeout:
        print(f"  Tentativa {numero_tentativa}: timeout, nenhum ACK recebido")
        return False


def exibir_cabecalho() -> None:
    """
    Exibe o cabeçalho de identificação do cliente no terminal
    """

    print(f"\n{'=' * 60}")
    print("CLIENTE UDP COM RETRANSMISSÃO")
    print(f"{'=' * 60}\n")


def exibir_resultado_final(mensagem: str, confirmada: bool, total_tentativas: int) -> None:
    """
    Exibe o resultado consolidado após o ciclo de tentativas de entrega

    Args:
        mensagem (str): Texto da mensagem que foi enviada
        confirmada (bool): Indica se a entrega foi confirmada pelo servidor
        total_tentativas (int): Número total de tentativas realizadas
    """

    print(f"\n  Resultado final:")
    print(f"    Mensagem: {mensagem}")
    print(f"    Total de tentativas: {total_tentativas}")

    if confirmada:
        print(f"    Entrega: confirmada com sucesso\n")

    else:
        print(f"    Entrega: falhou após {total_tentativas} tentativas\n")


def enviar_com_confirmacao(mensagem: str, host: str, porta: int, timeout: float, max_tentativas: int) -> None:
    """
    Coordena o envio confiável de uma mensagem UDP com retransmissão automática por timeout

    Args:
        mensagem (str): Texto da mensagem a enviar
        host (str): Endereço IP do servidor
        porta (int): Porta do servidor
        timeout (float): Tempo máximo de espera por ACK em cada tentativa
        max_tentativas (int): Número máximo de tentativas antes de desistir
    """

    dados = mensagem.encode("utf-8")
    endereco = (host, porta)
    confirmada = False

    with criar_socket_cliente(timeout) as sock:
        for tentativa in range(1, max_tentativas + 1):
            confirmada = tentar_envio(sock, dados, endereco, tentativa)

            if confirmada:
                break

    exibir_resultado_final(mensagem, confirmada, tentativa)


def executar_cliente(host: str, porta: int) -> None:
    """
    Inicializa o cliente UDP e realiza o envio confiável das mensagens configuradas

    Args:
        host (str): Endereço IP do servidor
        porta (int): Porta do servidor
    """

    mensagens: List[str] = [
        "Primeira mensagem de teste",
        "Segunda mensagem de teste",
        "Terceira mensagem de teste",
    ]

    exibir_cabecalho()
    print(f"  Servidor alvo: {host}:{porta}")
    print(f"  Timeout por tentativa: {TIMEOUT_SEGUNDOS}s")
    print(f"  Máximo de tentativas: {MAX_TENTATIVAS}\n")

    for mensagem in mensagens:
        print(f"  Enviando: \"{mensagem}\"")
        enviar_com_confirmacao(mensagem, host, porta, TIMEOUT_SEGUNDOS, MAX_TENTATIVAS)


executar_cliente(HOST_SERVIDOR, PORTA)
