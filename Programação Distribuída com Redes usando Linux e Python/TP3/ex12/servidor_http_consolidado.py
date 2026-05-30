import socket
import datetime
import threading
from typing import Tuple, Dict


HOST = "0.0.0.0"
PORTA = 8080

TAMANHO_BUFFER = 8192

ROTAS: Dict[str, Tuple[int, str, str]] = {
    "/": (
        200,
        "OK",
        (
            "<!DOCTYPE html>\r\n"
            "<html>\r\n"
            "  <head><meta charset='UTF-8'><title>OK</title></head>\r\n"
            "  <body><h1>200 - OK</h1></body>\r\n"
            "</html>"
        ),
    ),
    "/admin": (
        403,
        "Forbidden",
        (
            "<!DOCTYPE html>\r\n"
            "<html>\r\n"
            "  <head><meta charset='UTF-8'><title>Forbidden</title></head>\r\n"
            "  <body><h1>403 - Forbidden</h1></body>\r\n"
            "</html>"
        ),
    ),
}

CORPO_404 = (
    "<!DOCTYPE html>\r\n"
    "<html>\r\n"
    "  <head><meta charset='UTF-8'><title>Not Found</title></head>\r\n"
    "  <body><h1>404 - Not Found</h1></body>\r\n"
    "</html>"
)

LOG: list = []
lock_log = threading.Lock()
contador_requisicoes = 0
lock_contador = threading.Lock()


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


def proximo_id_requisicao() -> int:
    """
    Retorna o próximo identificador sequencial de requisição de forma thread-safe

    Returns:
        int: Identificador único da requisição
    """

    global contador_requisicoes

    with lock_contador:
        contador_requisicoes += 1
        return contador_requisicoes


def montar_resposta(status_code: int, status_text: str, corpo: str) -> bytes:
    """
    Monta a resposta HTTP/1.1 completa com status line, cabeçalhos obrigatórios e corpo

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
        str: Caminho extraído sem query string, ou string vazia se inválido
    """

    try:
        linha = requisicao.splitlines()[0]
        partes = linha.split(" ")

        if len(partes) >= 2:
            return partes[1].split("?")[0]

        return ""

    except (IndexError, AttributeError):
        return ""


def extrair_headers_requisicao(requisicao: str) -> Dict[str, str]:
    """
    Extrai os cabeçalhos HTTP da requisição recebida

    Args:
        requisicao (str): Texto bruto da requisição HTTP

    Returns:
        Dict[str, str]: Dicionário com chaves e valores dos cabeçalhos recebidos
    """

    headers = {}

    try:
        linhas = requisicao.splitlines()

        for linha in linhas[1:]:
            if not linha.strip():
                break

            if ":" in linha:
                chave, _, valor = linha.partition(":")
                headers[chave.strip()] = valor.strip()

    except Exception:
        pass

    return headers


def processar_requisicao(dados: bytes, id_req: int, horario: str) -> Tuple[bytes, int, str]:
    """
    Interpreta a requisição HTTP, registra as informações recebidas e retorna a resposta adequada

    Args:
        dados (bytes): Bytes brutos recebidos do cliente
        id_req (int): Identificador sequencial da requisição
        horario (str): Horário de recebimento da requisição

    Returns:
        Tuple[bytes, int, str]: Resposta serializada, código de status e caminho requisitado
    """

    requisicao = dados.decode("utf-8", errors="replace")
    metodo = extrair_metodo(requisicao)
    caminho = extrair_caminho(requisicao)
    headers = extrair_headers_requisicao(requisicao)

    registrar(f"  Req #{id_req:04d}  Horário: {horario}")
    registrar(f"  Método: {metodo}")
    registrar(f"  Caminho: {caminho}")

    if "User-Agent" in headers:
        registrar(f"  Agente: {headers['User-Agent'][:60]}")

    if "Host" in headers:
        registrar(f"  Host: {headers['Host']}")

    if metodo != "GET":
        corpo = f"<html><body><h1>405 - Método {metodo} não permitido</h1></body></html>"
        return montar_resposta(405, "Method Not Allowed", corpo), 405, caminho

    if caminho in ROTAS:
        status_code, status_text, corpo = ROTAS[caminho]
        return montar_resposta(status_code, status_text, corpo), status_code, caminho

    return montar_resposta(404, "Not Found", CORPO_404), 404, caminho


def atender_cliente(conexao: socket.socket, endereco: Tuple[str, int]) -> None:
    """
    Recebe a requisição de um cliente, registra horário e dados, processa e envia a resposta

    Args:
        conexao (socket.socket): Socket da conexão estabelecida
        endereco (Tuple[str, int]): IP e porta do cliente
    """

    horario_recebimento = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    id_req = proximo_id_requisicao()

    registrar(f"Requisição de {endereco[0]}:{endereco[1]}")

    try:
        dados = conexao.recv(TAMANHO_BUFFER)

        if not dados:
            return

        resposta, status_code, caminho = processar_requisicao(dados, id_req, horario_recebimento)
        conexao.sendall(resposta)

        registrar(f"  Resposta: {status_code}  ({len(resposta)} bytes)")

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"  Conexão encerrada abruptamente por {endereco[0]}")

    except OSError as e:
        registrar(f"  Erro na sessão com {endereco[0]}:{endereco[1]}: {e}")

    finally:
        conexao.close()
        registrar(f"  Conexão encerrada com {endereco[0]}:{endereco[1]}")


def iniciar_servidor() -> None:
    """
    Inicializa o servidor HTTP, aceita conexões em loop e despacha cada cliente para uma thread independente
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORTA))
        sock.listen(20)

        registrar(f"Servidor HTTP consolidado aguardando conexões em {HOST}:{PORTA}")
        registrar(f"Rotas configuradas: {', '.join(ROTAS.keys())} | qualquer outra: 404")

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
