import socket
import multiprocessing
import datetime
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 12345

TAMANHO_BUFFER = 4096

LOG: list = []
lock_log = multiprocessing.Lock()


def registrar(evento: str, lock: multiprocessing.Lock = None) -> None:
    """
    Registra um evento com timestamp no log e imprime no terminal

    Args:
        evento (str): Descrição do evento ocorrido
        lock (multiprocessing.Lock): Lock para sincronizar a escrita entre processos
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"

    if lock:
        with lock:
            print(entrada)
    else:
        LOG.append(entrada)
        print(entrada)


def handle_client(conexao: socket.socket, endereco: Tuple[str, int], lock: multiprocessing.Lock) -> None:
    """
    Trata a sessão completa de um cliente conectado, recebe mensagens, imprime os dados e devolve o echo

    Args:
        conexao (socket.socket): Socket da conexão estabelecida com o cliente
        endereco (Tuple[str, int]): IP e porta do cliente
        lock (multiprocessing.Lock): Lock compartilhado para escrita sincronizada no terminal
    """

    registrar(f"Processo {multiprocessing.current_process().pid} atendendo {endereco[0]}:{endereco[1]}", lock)

    try:
        while True:
            dados = conexao.recv(TAMANHO_BUFFER)

            if not dados:
                break

            mensagem = dados.decode("utf-8", errors="replace")

            registrar(
                f"  IP: {endereco[0]}  Porta: {endereco[1]}  Mensagem: {mensagem[:80]}{'...' if len(mensagem) > 80 else ''}",
                lock
            )

            conexao.sendall(dados)

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"  Conexão encerrada abruptamente por {endereco[0]}:{endereco[1]}", lock)

    except OSError as e:
        registrar(f"  Erro na sessão com {endereco[0]}:{endereco[1]}: {e}", lock)

    finally:
        conexao.close()
        registrar(f"  Sessão encerrada com {endereco[0]}:{endereco[1]}", lock)


def iniciar_servidor() -> None:
    """
    Inicializa o servidor TCP, aguarda conexões em loop e despacha cada cliente para um processo independente
    """

    lock = multiprocessing.Lock()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORTA))
        sock.listen(10)

        registrar(f"Servidor TCP aguardando conexões em {HOST}:{PORTA}")

        processos = []

        while True:
            try:
                conexao, endereco = sock.accept()
                registrar(f"Conexão aceita de {endereco[0]}:{endereco[1]}")

                processo = multiprocessing.Process(
                    target=handle_client,
                    args=(conexao, endereco, lock),
                    daemon=True
                )
                processo.start()
                processos.append(processo)

                conexao.close()
                processos = [p for p in processos if p.is_alive()]

            except OSError as e:
                registrar(f"Erro ao aceitar conexão: {e}")

    except OSError as e:
        registrar(f"Erro ao iniciar servidor: {e}")

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
