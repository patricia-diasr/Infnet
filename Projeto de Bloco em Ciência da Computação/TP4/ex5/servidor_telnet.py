import socket
import subprocess
import datetime
import threading
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 23

IAC = bytes([255])
WILL = bytes([251])
WONT = bytes([252])
DO = bytes([253])
DONT = bytes([254])

OPT_ECHO = bytes([1])
OPT_SUPRESS_GA = bytes([3])
OPT_TERMINAL = bytes([24])
OPT_NAWS = bytes([31])

BANNER = (
    "\r\n"
    "======================================\r\n"
    "  Servidor Telnet - Exercício de Redes\r\n"
    "======================================\r\n"
    "Digite 'ajuda' para ver os comandos disponíveis.\r\n"
    "Digite 'sair' para encerrar a sessão.\r\n\r\n"
)

COMANDOS_PERMITIDOS = {
    "data": ["date"],
    "hora": ["date", "+%H:%M:%S"],
    "quem": ["whoami"],
    "hostname": ["hostname"],
    "uptime": ["uptime", "-p"],
    "disco": ["df", "-h", "--total"],
    "memoria": ["free", "-h"],
    "processos": ["ps", "aux", "--sort=-%cpu"],
    "rede": ["ip", "addr", "show"],
    "ping": ["ping", "-c", "4", "8.8.8.8"],
}

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


def negociar_opcoes(conexao: socket.socket) -> None:
    """
    Envia as opções iniciais do protocolo Telnet para o cliente

    Args:
        conexao (socket.socket): Socket da conexão com o cliente
    """

    conexao.sendall(IAC + WILL + OPT_SUPRESS_GA)
    conexao.sendall(IAC + WILL + OPT_ECHO)
    conexao.sendall(IAC + DO + OPT_SUPRESS_GA)
    conexao.sendall(IAC + DONT + OPT_TERMINAL)
    conexao.sendall(IAC + DONT + OPT_NAWS)


def limpar_dados_telnet(dados: bytes) -> str:
    """
    Remove sequências IAC e caracteres de controle Telnet dos dados recebidos

    Args:
        dados (bytes): Bytes brutos recebidos do cliente

    Returns:
        str: Texto limpo sem sequências de protocolo
    """

    resultado = bytearray()
    i = 0

    while i < len(dados):
        if dados[i] == 255:
            if i + 2 < len(dados):
                i += 3

            else:
                i += 1

        elif dados[i] == 13:
            i += 1

        elif dados[i] == 10:
            resultado.extend(b"\n")
            i += 1

        elif dados[i] == 0:
            i += 1

        else:
            resultado.append(dados[i])
            i += 1

    return resultado.decode("utf-8", errors="ignore")


def executar_comando(comando: str) -> str:
    """
    Executa um comando permitido via subprocess e retorna a saída formatada

    Args:
        comando (str): Nome do comando digitado pelo cliente

    Returns:
        str: Saída do comando ou mensagem de erro/ajuda
    """

    comando = comando.strip().lower()

    if comando == "ajuda":
        linhas = ["\r\nComandos disponíveis:\r\n"]

        for nome in sorted(COMANDOS_PERMITIDOS):
            linhas.append(f"  {nome}\r\n")

        linhas.append("\r\n")
        return "".join(linhas)

    if comando not in COMANDOS_PERMITIDOS:
        return f"\r\nComando '{comando}' não reconhecido. Digite 'ajuda'.\r\n\r\n"

    try:
        resultado = subprocess.run(
            COMANDOS_PERMITIDOS[comando],
            capture_output=True,
            text=True,
            timeout=10
        )
        saida = resultado.stdout or resultado.stderr
        return "\r\n" + saida.replace("\n", "\r\n") + "\r\n"

    except subprocess.TimeoutExpired:
        return "\r\nErro: tempo limite excedido.\r\n\r\n"

    except Exception as e:
        return f"\r\nErro ao executar: {e}\r\n\r\n"


def atender_cliente(conexao: socket.socket, endereco: Tuple[str, int]) -> None:
    """
    Gerencia a sessão completa de um cliente conectado em thread separada

    Args:
        conexao (socket.socket): Socket da conexão estabelecida
        endereco (Tuple[str, int]): IP e porta do cliente
    """

    registrar(f"Sessão iniciada com {endereco[0]}:{endereco[1]}")

    try:
        negociar_opcoes(conexao)
        conexao.sendall(BANNER.encode("utf-8"))
        conexao.sendall(b"$ ")
        buffer = b""

        while True:
            fragmento = conexao.recv(256)

            if not fragmento:
                break

            buffer += fragmento
            texto = limpar_dados_telnet(buffer)

            while "\n" in texto:
                comando, texto = texto.split("\n", 1)
                buffer = texto.encode("utf-8")
                comando = comando.strip()

                if not comando:
                    conexao.sendall(b"$ ")
                    continue

                registrar(f"Comando de {endereco[0]}: '{comando}'")

                if comando == "sair":
                    conexao.sendall("\r\nEncerrando sessão. Até logo.\r\n".encode("utf-8"))
                    return

                resposta = executar_comando(comando)
                conexao.sendall(resposta.encode("utf-8"))
                conexao.sendall(b"$ ")
                texto = limpar_dados_telnet(buffer)

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"Conexão encerrada abruptamente por {endereco[0]}")

    finally:
        conexao.close()
        registrar(f"Sessão encerrada com {endereco[0]}:{endereco[1]}")


def iniciar_servidor() -> None:
    """
    Inicializa o servidor Telnet e aguarda conexões em loop, criando uma thread por cliente
    """

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)

    registrar(f"Servidor Telnet aguardando conexões em {HOST}:{PORTA}")

    try:
        while True:
            conexao, endereco = servidor.accept()
            thread = threading.Thread(
                target=atender_cliente,
                args=(conexao, endereco),
                daemon=True
            )
            thread.start()

    except KeyboardInterrupt:
        registrar("Servidor encerrado pelo operador")

    finally:
        servidor.close()
        exibir_log()


def exibir_log() -> None:
    """
    Exibe o histórico completo de eventos ao encerrar o servidor
    """

    print("\n===== Log completo da sessão Telnet =====\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor()
