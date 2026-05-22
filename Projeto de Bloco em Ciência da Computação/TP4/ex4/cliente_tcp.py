import socket
from typing import List


HOST_SERVIDOR = "192.168.56.101"
PORTA = 5000
TAMANHO_BUFFER = 1024


def enviar_mensagem_tcp(mensagem: str) -> str:
    """
    Abre uma conexão TCP, envia uma mensagem e retorna a resposta do servidor

    Args:
        mensagem (str): Texto a ser enviado ao servidor

    Returns:
        str: Resposta recebida do servidor, ou mensagem de erro em caso de falha
    """

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST_SERVIDOR, PORTA))
        cliente.sendall(mensagem.encode("utf-8"))
        resposta = cliente.recv(TAMANHO_BUFFER).decode("utf-8")
        cliente.close()
        return resposta

    except ConnectionRefusedError:
        return "Erro: servidor não encontrado ou porta recusada"

    except Exception as e:
        return f"Erro inesperado: {e}"


def executar_bateria_tcp(mensagens: List[str]) -> None:
    """
    Envia uma lista de mensagens ao servidor TCP e exibe os resultados em tabela

    Args:
        mensagens (List[str]): Lista de mensagens a enviar
    """

    col_n = 5
    col_msg = 70
    col_resp = 100

    sep = f"+{'-' * (col_n + 2)}+{'-' * (col_msg + 2)}+{'-' * (col_resp + 2)}+"
    cab = (f"| {'#':^{col_n}} | {'Mensagem enviada':^{col_msg}} | {'Resposta recebida':^{col_resp}} |")

    print("\n===== Bateria de testes TCP =====\n")
    print(sep)
    print(cab)
    print(sep)

    for i, mensagem in enumerate(mensagens, 1):
        resposta = enviar_mensagem_tcp(mensagem)
        print(f"| {str(i):^{col_n}} | {mensagem:<{col_msg}} | {resposta:<{col_resp}} |")

    print(sep)
    print()


MENSAGENS_TESTE = [
    "Olá, servidor TCP",
    "Testando conexão 1",
    "Testando conexão 2",
    "Testando conexão 3",
    "Mensagem com acentuação",
    "Número: 12345",
    "Mensagem longa: " + "A" * 50,
    "Última mensagem de teste"
]

executar_bateria_tcp(MENSAGENS_TESTE)
