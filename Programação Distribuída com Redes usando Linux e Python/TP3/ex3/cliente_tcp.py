import socket
import datetime
import sys


HOST_SERVIDOR = "192.168.56.101"
PORTA = 12345

TAMANHO_BUFFER = 4096

LOG: list = []


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log da execução

    Args:
        evento (str): Descrição do evento ocorrido
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"
    LOG.append(entrada)
    print(entrada)


def montar_mensagem(id_cliente: str) -> str:
    """
    Monta a mensagem a ser enviada ao servidor com pelo menos 10 bytes

    Args:
        id_cliente (str): Identificador do cliente, usado como prefixo da mensagem

    Returns:
        str: Mensagem formatada com no mínimo 10 bytes ao ser codificada em UTF-8
    """

    corpo = f"Cliente {id_cliente} conectado ao servidor TCP"
    return corpo


def executar_cliente(id_cliente: str) -> None:
    """
    Conecta ao servidor TCP, exibe o endereço local via getsockname, envia a mensagem e imprime o echo recebido

    Args:
        id_cliente (str): Identificador textual do cliente para compor a mensagem
    """

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST_SERVIDOR, PORTA))

        ip_local, porta_local = sock.getsockname()
        registrar(f"Conectado ao servidor {HOST_SERVIDOR}:{PORTA}")
        registrar(f"Endereço local (getsockname): {ip_local}:{porta_local}")

        mensagem = montar_mensagem(id_cliente)
        payload = mensagem.encode("utf-8")

        registrar(f"Enviando mensagem ({len(payload)} bytes): {mensagem}")
        sock.sendall(payload)

        echo = sock.recv(TAMANHO_BUFFER)
        resposta = echo.decode("utf-8", errors="replace")

        registrar(f"Echo recebido ({len(echo)} bytes): {resposta}")

        integro = echo == payload
        registrar(f"Integridade do echo: {'íntegro' if integro else 'divergente'}")

    except ConnectionRefusedError:
        registrar(f"Erro: conexão recusada em {HOST_SERVIDOR}:{PORTA}")

    except OSError as e:
        registrar(f"Erro de socket: {e}")

    finally:
        if sock:
            sock.close()
            registrar("Socket encerrado")

        exibir_log()


def exibir_log() -> None:
    """
    Exibe o log completo da execução ao final do programa
    """

    print(f"\n{'=' * 100}")
    print("LOG DA EXECUÇÃO")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


id_cliente = sys.argv[1] if len(sys.argv) > 1 else "1"
executar_cliente(id_cliente)
