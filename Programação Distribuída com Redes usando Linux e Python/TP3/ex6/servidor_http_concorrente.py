import socket
import multiprocessing
import datetime
from typing import Tuple, Dict


HOST = "0.0.0.0"
PORTA = 8080

TAMANHO_BUFFER = 4096

ROTAS: Dict[str, str] = {
    "/": (
        "<!DOCTYPE html>\r\n"
        "<html>\r\n"
        "  <head><meta charset='UTF-8'><title>Raiz</title></head>\r\n"
        "  <body><h1>RAIZ</h1></body>\r\n"
        "</html>"
    ),
    "/health": (
        "<!DOCTYPE html>\r\n"
        "<html>\r\n"
        "  <head><meta charset='UTF-8'><title>Health</title></head>\r\n"
        "  <body><h1>HEALTH</h1></body>\r\n"
        "</html>"
    ),
}

RESPOSTA_404 = (
    "<!DOCTYPE html>\r\n"
    "<html>\r\n"
    "  <head><meta charset='UTF-8'><title>Não encontrado</title></head>\r\n"
    "  <body><h1>404 - Recurso não encontrado</h1></body>\r\n"
    "</html>"
)

LOG: list = []
lock_log = multiprocessing.Lock()


def registrar(evento: str, lock: multiprocessing.Lock = None) -> None:
    """
    Registra um evento com timestamp no log e imprime no terminal de forma sincronizada entre processos

    Args:
        evento (str): Descrição do evento ocorrido
        lock (multiprocessing.Lock): Lock para serializar a escrita entre processos concorrentes
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [PID {multiprocessing.current_process().pid}] {evento}"

    if lock:
        with lock:
            print(entrada)

    else:
        LOG.append(entrada)
        print(entrada)


def montar_resposta(status_code: int, status_text: str, corpo: str) -> bytes:
    """
    Monta a resposta HTTP/1.1 completa com status line, headers obrigatórios e corpo

    Args:
        status_code (int): Código de status HTTP
        status_text (str): Texto descritivo do status
        corpo (str): Conteúdo HTML do corpo da resposta

    Returns:
        bytes: Resposta HTTP completa pronta para envio via socket
    """

    payload = corpo.encode("utf-8")
    data_hora = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    status_line = f"HTTP/1.1 {status_code} {status_text}\r\n"
    headers = (
        f"Date: {data_hora}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(payload)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    return (status_line + headers).encode("utf-8") + payload


def extrair_metodo(requisicao: str) -> str:
    """
    Extrai o método HTTP da linha de requisição

    Args:
        requisicao (str): Texto bruto da requisição HTTP

    Returns:
        str: Método HTTP em maiúsculas, ou string vazia se inválido
    """

    try:
        return requisicao.splitlines()[0].split(" ")[0].upper()

    except (IndexError, AttributeError):
        return ""


def extrair_caminho(requisicao: str) -> str:
    """
    Extrai o caminho da URL da linha de requisição HTTP

    Args:
        requisicao (str): Texto bruto da requisição HTTP

    Returns:
        str: Caminho extraído, ou string vazia se o formato for inválido
    """

    try:
        linha = requisicao.splitlines()[0]
        partes = linha.split(" ")

        if len(partes) >= 2:
            return partes[1]

        return ""

    except (IndexError, AttributeError):
        return ""


def processar_requisicao(dados: bytes) -> bytes:
    """
    Interpreta a requisição HTTP recebida e retorna a resposta adequada ao caminho e método solicitados

    Args:
        dados (bytes): Bytes brutos recebidos do cliente

    Returns:
        bytes: Resposta HTTP completa serializada
    """

    requisicao = dados.decode("utf-8", errors="replace")
    metodo = extrair_metodo(requisicao)
    caminho = extrair_caminho(requisicao)

    if metodo != "GET":
        corpo = f"<html><body><h1>405 - Método {metodo} não permitido</h1></body></html>"
        return montar_resposta(405, "Method Not Allowed", corpo)

    if caminho in ROTAS:
        return montar_resposta(200, "OK", ROTAS[caminho])

    return montar_resposta(404, "Not Found", RESPOSTA_404)


def handle_client(conexao: socket.socket, endereco: Tuple[str, int], lock: multiprocessing.Lock) -> None:
    """
    Trata a sessão completa de um cliente em processo independente, recebe a requisição, processa e envia a resposta

    Args:
        conexao (socket.socket): Socket da conexão estabelecida com o cliente
        endereco (Tuple[str, int]): IP e porta do cliente
        lock (multiprocessing.Lock): Lock compartilhado para escrita sincronizada no terminal
    """

    registrar(f"Atendendo {endereco[0]}:{endereco[1]}", lock)

    try:
        dados = conexao.recv(TAMANHO_BUFFER)

        if not dados:
            return

        requisicao = dados.decode("utf-8", errors="replace")
        linha_req = requisicao.splitlines()[0] if requisicao.splitlines() else "(vazia)"

        registrar(f"  Requisição: {linha_req}", lock)

        resposta = processar_requisicao(dados)
        conexao.sendall(resposta)

        registrar(f"  Resposta enviada ({len(resposta)} bytes)", lock)

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"  Conexão encerrada abruptamente por {endereco[0]}", lock)

    except OSError as e:
        registrar(f"  Erro na sessão com {endereco[0]}:{endereco[1]}: {e}", lock)

    finally:
        conexao.close()
        registrar(f"  Conexão encerrada com {endereco[0]}:{endereco[1]}", lock)


def iniciar_servidor() -> None:
    """
    Inicializa o servidor HTTP concorrente, aceita conexões em loop e despacha cada cliente para um processo independente via multiprocessing.Process
    """

    lock = multiprocessing.Lock()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORTA))
        sock.listen(20)

        registrar(f"Servidor HTTP/1.1 concorrente aguardando conexões em {HOST}:{PORTA}", lock)
        registrar(f"Rotas disponíveis: {', '.join(ROTAS.keys())}", lock)

        processos = []

        while True:
            try:
                conexao, endereco = sock.accept()

                processo = multiprocessing.Process(
                    target=handle_client,
                    args=(conexao, endereco, lock),
                    daemon=True
                )
                processo.start()
                processos.append(processo)

                conexao.close()

                processos = [p for p in processos if p.is_alive()]

                registrar(f"Processos ativos: {len(processos)}", lock)

            except OSError as e:
                registrar(f"Erro ao aceitar conexão: {e}", lock)

    except OSError as e:
        registrar(f"Erro ao iniciar servidor: {e}", lock)

    except KeyboardInterrupt:
        registrar("Servidor encerrado pelo operador", lock)

    finally:
        sock.close()
        exibir_log()


def exibir_log() -> None:
    """
    Exibe o log de eventos registrados no processo principal ao encerrar o servidor
    """

    print(f"\n{'=' * 100}")
    print("LOG DA EXECUÇÃO")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor()
