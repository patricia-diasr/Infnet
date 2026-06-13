import socket
import datetime
from typing import Tuple, Dict


HOST = "0.0.0.0"
PORTA = 8080
ARQUIVO_LOG = "acessos.log"

CONTEUDOS: Dict[str, Dict[str, str]] = {
    "/home.html": {
        "pt": "<html><body><h1>Página inicial</h1><p>Bem vindo ao nosso site</p></body></html>",
        "en": "<html><body><h1>Home page</h1><p>Welcome to our website</p></body></html>",
    },
    "/contato.html": {
        "pt": "<html><body><h1>Contato</h1><p>Envie sua mensagem pelo formulário abaixo</p></body></html>",
        "en": "<html><body><h1>Contact</h1><p>Send your message using the form below</p></body></html>",
    },
}


def parsear_requisicao(dados: bytes) -> Tuple[str, str, Dict[str, str]]:
    """
    Interpreta os bytes brutos de uma requisição HTTP e extrai método, caminho e cabeçalhos

    Args:
        dados (bytes): Bytes brutos recebidos do socket do cliente

    Returns:
        Tuple[str, str, Dict[str, str]]: (método HTTP, caminho solicitado, dicionário de cabeçalhos)
    """

    texto = dados.decode("utf-8", errors="replace")
    linhas = texto.split("\r\n")
    primeira_linha = linhas[0].split(" ")

    metodo = primeira_linha[0] if len(primeira_linha) > 0 else ""
    caminho = primeira_linha[1] if len(primeira_linha) > 1 else ""

    cabecalhos: Dict[str, str] = {}

    for linha in linhas[1:]:
        if ":" in linha:
            chave, _, valor = linha.partition(":")
            cabecalhos[chave.strip().lower()] = valor.strip()

    return metodo, caminho, cabecalhos


def detectar_idioma(cabecalhos: Dict[str, str]) -> str:
    """
    Determina o idioma da resposta com base no cabeçalho Accept Language da requisição

    Args:
        cabecalhos (Dict[str, str]): Cabeçalhos HTTP da requisição

    Returns:
        str: Código do idioma identificado, podendo ser pt ou en
    """

    accept_language = cabecalhos.get("accept-language", "")

    if "en" in accept_language.lower():
        return "en"

    return "pt"


def montar_resposta(metodo: str, caminho: str, idioma: str) -> Tuple[bytes, int]:
    """
    Monta a resposta HTTP completa com base no método, caminho e idioma da requisição

    Args:
        metodo (str): Método HTTP identificado na requisição
        caminho (str): Caminho solicitado na requisição
        idioma (str): Código do idioma identificado para a resposta

    Returns:
        Tuple[bytes, int]: (resposta HTTP serializada em bytes, código de status retornado)
    """

    if not metodo or not caminho:
        corpo = "<html><body><h1>400 Requisição inválida</h1></body></html>"
        status_code = 400
        status_texto = "Bad Request"

    elif metodo != "GET":
        corpo = "<html><body><h1>405 Método não permitido</h1></body></html>"
        status_code = 405
        status_texto = "Method Not Allowed"

    elif caminho not in CONTEUDOS:
        corpo = "<html><body><h1>404 Página não encontrada</h1></body></html>"
        status_code = 404
        status_texto = "Not Found"

    else:
        corpo = CONTEUDOS[caminho][idioma]
        status_code = 200
        status_texto = "OK"

    corpo_bytes = corpo.encode("utf-8")

    cabecalho = (
        f"HTTP/1.1 {status_code} {status_texto}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(corpo_bytes)}\r\n"
        f"Content-Language: {idioma}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    return cabecalho.encode("utf-8") + corpo_bytes, status_code


def registrar_acesso(caminho_log: str, ip: str, metodo: str, endpoint: str, status: int) -> None:
    """
    Registra uma linha de log estruturado para a requisição atendida

    Args:
        caminho_log (str): Caminho do arquivo de log de acessos
        ip (str): Endereço IP do cliente
        metodo (str): Método HTTP da requisição
        endpoint (str): Caminho solicitado na requisição
        status (int): Código de status HTTP retornado
    """

    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{timestamp} | {ip} | {metodo} | {endpoint} | {status}\n"

    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def atender_cliente(conn: socket.socket, endereco: Tuple[str, int], caminho_log: str) -> None:
    """
    Atende uma conexão de cliente, processa a requisição e envia a resposta correspondente

    Args:
        conn (socket.socket): Socket da conexão com o cliente
        endereco (Tuple[str, int]): Endereço IP e porta do cliente
        caminho_log (str): Caminho do arquivo de log de acessos
    """

    with conn:
        dados = conn.recv(4096)

        if not dados:
            return

        metodo, caminho, cabecalhos = parsear_requisicao(dados)
        idioma = detectar_idioma(cabecalhos)
        resposta, status = montar_resposta(metodo, caminho, idioma)

        conn.sendall(resposta)
        registrar_acesso(caminho_log, endereco[0], metodo or "?", caminho or "?", status)

        print(f"  {endereco[0]} solicitou {metodo} {caminho} e recebeu status {status}")


def criar_socket_servidor(host: str, porta: int) -> socket.socket:
    """
    Cria e configura o socket TCP do servidor pronto para aceitar conexões HTTP

    Args:
        host (str): Endereço de escuta do servidor
        porta (int): Porta de escuta do servidor

    Returns:
        socket.socket: Socket configurado e em modo de escuta
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, porta))
    sock.listen(5)
    return sock


def executar_servidor(host: str, porta: int, caminho_log: str) -> None:
    """
    Inicializa o servidor HTTP e entra em loop aguardando conexões dos clientes

    Args:
        host (str): Endereço de escuta do servidor
        porta (int): Porta de escuta do servidor
        caminho_log (str): Caminho do arquivo de log de acessos
    """

    sock = criar_socket_servidor(host, porta)

    print(f"\n{'=' * 60}")
    print("SERVIDOR HTTP INSTRUMENTADO")
    print(f"{'=' * 60}")
    print(f"\n  Aguardando conexões em {host}:{porta}")
    print(f"  Log de acessos em {caminho_log}\n")

    while True:
        conn, endereco = sock.accept()
        atender_cliente(conn, endereco, caminho_log)


executar_servidor(HOST, PORTA, ARQUIVO_LOG)
