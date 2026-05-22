import socket
import datetime
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 5001
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


def iniciar_servidor_udp() -> None:
    """
    Inicia o servidor UDP, aguarda datagramas e responde a cada remetente em loop
    """

    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORTA))
    registrar(f"Servidor UDP aguardando datagramas em {HOST}:{PORTA}")

    try:
        while True:
            dados, endereco_cliente = servidor.recvfrom(TAMANHO_BUFFER)
            tratar_datagrama_udp(servidor, dados, endereco_cliente)

    except KeyboardInterrupt:
        registrar("Servidor UDP encerrado pelo operador")

    finally:
        servidor.close()
        exibir_log()


def tratar_datagrama_udp(servidor: socket.socket, dados: bytes, endereco: Tuple[str, int]) -> None:
    """
    Processa um datagrama recebido, registra e envia resposta ao remetente

    Args:
        servidor (socket.socket): Socket do servidor para envio da resposta
        dados (bytes): Conteúdo bruto do datagrama recebido
        endereco (Tuple[str, int]): Endereço IP e porta do remetente
    """

    mensagem = dados.decode("utf-8")
    registrar(f"Datagrama recebido de {endereco[0]}:{endereco[1]} — '{mensagem}'")
    resposta = f"[UDP] Servidor recebeu: '{mensagem}'"
    servidor.sendto(resposta.encode("utf-8"), endereco)
    registrar(f"Resposta enviada para {endereco[0]}:{endereco[1]}")


def exibir_log() -> None:
    """
    Exibe o histórico completo de eventos registrados durante a execução
    """

    print("\n===== Log completo da sessão UDP =====\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor_udp()
