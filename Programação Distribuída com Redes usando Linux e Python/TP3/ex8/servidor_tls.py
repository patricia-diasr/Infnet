import ssl
import socket
import datetime
import threading
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 8443

ARQUIVO_CERT = "server.crt"
ARQUIVO_CHAVE = "server.key"

TAMANHO_BUFFER = 4096

RESPOSTA_CORPO = "Resposta via TLS local"

RESPOSTA_HTML = (
    "<!DOCTYPE html>\r\n"
    "<html>\r\n"
    "  <head><meta charset='UTF-8'><title>Servidor TLS</title></head>\r\n"
    f"  <body><h1>{RESPOSTA_CORPO}</h1></body>\r\n"
    "</html>"
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


def criar_contexto_tls() -> ssl.SSLContext:
    """
    Cria e configura o contexto TLS do servidor carregando o certificado e a chave privada

    Returns:
        ssl.SSLContext: Contexto TLS pronto para uso no servidor
    """

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain(certfile=ARQUIVO_CERT, keyfile=ARQUIVO_CHAVE)
    contexto.minimum_version = ssl.TLSVersion.TLSv1_2

    return contexto


def montar_resposta_http(corpo: str) -> bytes:
    """
    Monta uma resposta HTTP/1.1 completa com os cabeçalhos obrigatórios e o corpo fornecido

    Args:
        corpo (str): Conteúdo HTML do corpo da resposta

    Returns:
        bytes: Resposta HTTP completa pronta para envio via socket TLS
    """

    payload = corpo.encode("utf-8")
    data_hora = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    status_line = "HTTP/1.1 200 OK\r\n"
    headers = (
        f"Date: {data_hora}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(payload)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    return (status_line + headers).encode("utf-8") + payload


def atender_cliente(conexao_tls: ssl.SSLSocket, endereco: Tuple[str, int]) -> None:
    """
    Recebe a requisição do cliente, registra os dados da sessão TLS e envia a resposta

    Args:
        conexao_tls (ssl.SSLSocket): Socket TLS já com handshake concluído
        endereco (Tuple[str, int]): IP e porta do cliente
    """

    registrar(f"Conexão TLS estabelecida com {endereco[0]}:{endereco[1]}")

    try:
        versao = conexao_tls.version()
        cipher = conexao_tls.cipher()

        registrar(f"  Versão TLS: {versao}")
        registrar(f"  Cipher: {cipher[0]}  {cipher[1]}  {cipher[2]} bits")

        dados = conexao_tls.recv(TAMANHO_BUFFER)

        if not dados:
            return

        requisicao = dados.decode("utf-8", errors="replace")
        linha_req = requisicao.splitlines()[0] if requisicao.splitlines() else "(vazia)"

        registrar(f"  Requisição: {linha_req}")

        resposta = montar_resposta_http(RESPOSTA_HTML)
        conexao_tls.sendall(resposta)

        registrar(f"  Resposta enviada ({len(resposta)} bytes)")

    except ssl.SSLError as e:
        registrar(f"  Erro TLS com {endereco[0]}: {e}")

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"  Conexão encerrada abruptamente por {endereco[0]}")

    except OSError as e:
        registrar(f"  Erro de socket com {endereco[0]}: {e}")

    finally:
        conexao_tls.close()
        registrar(f"  Conexão encerrada com {endereco[0]}:{endereco[1]}")


def iniciar_servidor() -> None:
    """
    Inicializa o servidor TLS, aguarda conexões em loop e despacha cada cliente para uma thread independente
    """

    try:
        contexto = criar_contexto_tls()
        sock_raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_raw.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_raw.bind((HOST, PORTA))
        sock_raw.listen(10)

        registrar(f"Servidor TLS aguardando conexões em {HOST}:{PORTA}")
        registrar(f"Certificado: {ARQUIVO_CERT}")
        registrar(f"Chave: {ARQUIVO_CHAVE}")

        with contexto.wrap_socket(sock_raw, server_side=True) as sock_tls:
            while True:
                try:
                    conexao, endereco = sock_tls.accept()

                    thread = threading.Thread(
                        target=atender_cliente,
                        args=(conexao, endereco),
                        daemon=True
                    )
                    thread.start()

                except ssl.SSLError as e:
                    registrar(f"Erro TLS ao aceitar conexão: {e}")

                except OSError as e:
                    registrar(f"Erro ao aceitar conexão: {e}")

    except FileNotFoundError as e:
        registrar(f"Erro: arquivo de certificado ou chave não encontrado: {e}")

    except ssl.SSLError as e:
        registrar(f"Erro ao configurar contexto TLS: {e}")

    except OSError as e:
        registrar(f"Erro ao iniciar servidor: {e}")

    except KeyboardInterrupt:
        registrar("Servidor encerrado pelo operador")

    finally:
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
