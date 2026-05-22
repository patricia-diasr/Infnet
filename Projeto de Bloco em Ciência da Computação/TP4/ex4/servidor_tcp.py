import socket
import datetime
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 5000
TAMANHO_BUFFER = 1024
LOG: list = []


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log interno e exibe no terminal

    Args:
        evento (str): Descrição do evento ocorrido
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"
    LOG.append(entrada)
    print(entrada)


def iniciar_servidor_tcp() -> None:
    """
    Inicia o servidor TCP, aguarda conexões e responde a cada cliente em loop
    """

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    registrar(f"Servidor TCP aguardando conexões em {HOST}:{PORTA}")

    try:
        while True:
            conexao, endereco_cliente = servidor.accept()
            tratar_cliente_tcp(conexao, endereco_cliente)

    except KeyboardInterrupt:
        registrar("Servidor TCP encerrado pelo operador")

    finally:
        servidor.close()
        exibir_log()


def tratar_cliente_tcp(conexao: socket.socket, endereco: Tuple[str, int]) -> None:
    """
    Recebe a mensagem de um cliente conectado, registra e envia resposta

    Args:
        conexao (socket.socket): Socket da conexão estabelecida com o cliente
        endereco (Tuple[str, int]): Endereço IP e porta do cliente
    """

    registrar(f"Conexão estabelecida com {endereco[0]}:{endereco[1]}")

    try:
        dados = conexao.recv(TAMANHO_BUFFER)

        if dados:
            mensagem = dados.decode("utf-8")
            registrar(f"Mensagem recebida de {endereco[0]}: '{mensagem}'")
            resposta = f"[TCP] Servidor recebeu: '{mensagem}'"
            conexao.sendall(resposta.encode("utf-8"))
            registrar(f"Resposta enviada para {endereco[0]}")

    finally:
        conexao.close()
        registrar(f"Conexão encerrada com {endereco[0]}:{endereco[1]}")


def exibir_log() -> None:
    """
    Exibe o histórico completo de eventos registrados durante a execução
    """

    print("\n===== Log completo da sessão TCP =====\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor_tcp()
