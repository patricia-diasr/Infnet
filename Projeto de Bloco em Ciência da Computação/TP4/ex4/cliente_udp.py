import socket
from typing import List


HOST_SERVIDOR = "192.168.56.101"
PORTA = 5001
TAMANHO_BUFFER = 1024
TIMEOUT = 3.0


def enviar_datagrama_udp(mensagem: str) -> str:
    """
    Envia um datagrama UDP ao servidor e aguarda resposta dentro do timeout

    Args:
        mensagem (str): Texto a ser enviado ao servidor

    Returns:
        str: Resposta recebida do servidor, ou mensagem de erro/timeout
    """

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cliente.settimeout(TIMEOUT)
        cliente.sendto(mensagem.encode("utf-8"), (HOST_SERVIDOR, PORTA))
        resposta, _ = cliente.recvfrom(TAMANHO_BUFFER)
        cliente.close()
        return resposta.decode("utf-8")

    except socket.timeout:
        return f"Erro: sem resposta após {TIMEOUT}s (timeout)"

    except Exception as e:
        return f"Erro inesperado: {e}"


def executar_bateria_udp(mensagens: List[str]) -> None:
    """
    Envia uma lista de datagramas ao servidor UDP e exibe os resultados em tabela

    Args:
        mensagens (List[str]): Lista de mensagens a enviar
    """

    col_n = 5
    col_msg = 70
    col_resp = 100

    sep = f"+{'-' * (col_n + 2)}+{'-' * (col_msg + 2)}+{'-' * (col_resp + 2)}+"
    cab = (f"| {'#':^{col_n}} | {'Mensagem enviada':^{col_msg}} | {'Resposta recebida':^{col_resp}} |")

    print("\n===== Bateria de testes UDP =====\n")
    print(sep)
    print(cab)
    print(sep)

    for i, mensagem in enumerate(mensagens, 1):
        resposta = enviar_datagrama_udp(mensagem)
        print(f"| {str(i):^{col_n}} | {mensagem:<{col_msg}} | {resposta:<{col_resp}} |")

    print(sep)
    print()


MENSAGENS_TESTE = [
    "Olá, servidor UDP",
    "Testando conexão 1",
    "Testando conexão 2",
    "Testando conexão 3",
    "Mensagem com acentuação",
    "Número: 12345",
    "Mensagem longa: " + "A" * 50,
    "Última mensagem de teste"
]

executar_bateria_udp(MENSAGENS_TESTE)
