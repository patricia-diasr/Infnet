import socket
import threading
import datetime
from typing import Tuple


HOST = "::1"
PORTA = 12346

TAMANHO_BUFFER = 4096

BANNER = (
    "\r\n"
    "======================================\r\n"
    "Servidor TCP IPv6 - Exercício 9\r\n"
    "======================================\r\n"
    "Envie uma mensagem. Digite 'sair' para encerrar.\r\n\r\n"
)

LOG: list = []
lock_log = threading.Lock()


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log compartilhado entre threads

    Args:
        evento (str): Descrição do evento ocorrido
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"

    with lock_log:
        LOG.append(entrada)
        print(entrada)


def exibir_info_socket(sock: socket.socket) -> None:
    """
    Exibe as informações do socket recém-criado, incluindo família e tipo

    Args:
        sock (socket.socket): Socket a inspecionar
    """

    registrar(f"  Família: {sock.family.name}")
    registrar(f"  Tipo: {sock.type.name}")


def atender_cliente(conexao: socket.socket, endereco: Tuple) -> None:
    """
    Trata a sessão completa de um cliente IPv6 conectado, recebe mensagens, imprime os dados e devolve o echo

    Args:
        conexao (socket.socket): Socket da conexão estabelecida com o cliente
        endereco (Tuple): Tupla com IP, porta, flow info e scope id do cliente IPv6
    """

    ip_cliente = endereco[0]
    porta_cliente = endereco[1]

    registrar(f"Sessão iniciada com [{ip_cliente}]:{porta_cliente}")

    try:
        conexao.sendall(BANNER.encode("utf-8"))

        while True:
            dados = conexao.recv(TAMANHO_BUFFER)

            if not dados:
                break

            mensagem = dados.decode("utf-8", errors="replace").strip()

            registrar(f"  IP origem: {ip_cliente}")
            registrar(f"  Porta: {porta_cliente}")
            registrar(f"  Mensagem: {mensagem[:80]}{'...' if len(mensagem) > 80 else ''}")
            registrar(f"  Bytes: {len(dados)}")

            if mensagem.lower() == "sair":
                conexao.sendall("Encerrando sessão. Até logo.\r\n".encode("utf-8"))
                break

            conexao.sendall(dados)

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"  Conexão encerrada abruptamente por [{ip_cliente}]")

    except OSError as e:
        registrar(f"  Erro na sessão com [{ip_cliente}]:{porta_cliente}: {e}")

    finally:
        conexao.close()
        registrar(f"Sessão encerrada com [{ip_cliente}]:{porta_cliente}")


def verificar_suporte_ipv6() -> bool:
    """
    Verifica se o sistema operacional suporta IPv6 tentando criar um socket AF_INET6

    Returns:
        bool: True se IPv6 estiver disponível, False caso contrário
    """

    try:
        sock_teste = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock_teste.close()
        registrar("Suporte a IPv6 disponível no sistema operacional")
        return True

    except OSError as e:
        registrar(f"IPv6 não disponível no sistema operacional: {e}")
        return False


def iniciar_servidor() -> None:
    """
    Verifica suporte a IPv6, inicializa o servidor TCP no loopback ::1 e despacha cada cliente para uma thread independente
    """

    if not verificar_suporte_ipv6():
        registrar("Abortando: servidor IPv6 não pode ser iniciado sem suporte do sistema")
        exibir_log()
        return

    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

        exibir_info_socket(sock)

        sock.bind((HOST, PORTA, 0, 0))
        sock.listen(10)

        endereco_local = sock.getsockname()
        registrar(f"Servidor IPv6 aguardando conexões em [{endereco_local[0]}]:{endereco_local[1]}")

        while True:
            try:
                conexao, endereco = sock.accept()

                thread = threading.Thread(
                    target=atender_cliente,
                    args=(conexao, endereco),
                    daemon=True
                )
                thread.start()

            except OSError as e:
                registrar(f"Erro ao aceitar conexão: {e}")

    except OSError as e:
        registrar(f"Erro ao iniciar servidor IPv6: {e}")

    except KeyboardInterrupt:
        registrar("Servidor encerrado pelo operador")

    finally:
        sock.close()
        exibir_log()


def exibir_log() -> None:
    """
    Exibe o log completo da execução ao encerrar o servidor
    """

    print(f"\n{'=' * 100}")
    print("LOG DA EXECUÇÃO")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor()
