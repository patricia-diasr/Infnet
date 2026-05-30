import ssl
import socket
import datetime
from typing import Dict, Tuple


HOST_SERVIDOR = "127.0.0.1"
PORTA = 8443

ARQUIVO_CERT = "server.crt"

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


def montar_requisicao(caminho: str, host: str) -> bytes:
    """
    Monta uma requisição GET HTTP/1.1 mínima válida

    Args:
        caminho (str): Caminho do recurso a requisitar
        host (str): Valor do cabeçalho Host

    Returns:
        bytes: Requisição HTTP serializada
    """

    requisicao = (
        f"GET {caminho} HTTP/1.1\r\n"
        f"Host: {host}:{PORTA}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return requisicao.encode("utf-8")


def extrair_status(dados: bytes) -> str:
    """
    Extrai a status line da resposta HTTP recebida

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        str: Status line extraída ou indicação de ausência
    """

    try:
        return dados.decode("utf-8", errors="replace").splitlines()[0]

    except (IndexError, UnicodeDecodeError):
        return "(sem status)"


def extrair_headers(dados: bytes) -> Dict[str, str]:
    """
    Extrai o dicionário de headers da resposta HTTP recebida

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        Dict[str, str]: Dicionário com chaves e valores dos cabeçalhos HTTP
    """

    headers = {}

    try:
        texto = dados.decode("utf-8", errors="replace")
        pos = texto.find("\r\n\r\n")

        if pos == -1:
            return headers

        for linha in texto[:pos].splitlines()[1:]:
            if ":" in linha:
                chave, _, valor = linha.partition(":")
                headers[chave.strip()] = valor.strip()

    except Exception:
        pass

    return headers


def extrair_corpo(dados: bytes) -> str:
    """
    Extrai o corpo da resposta HTTP a partir do separador de cabeçalho

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        str: Corpo da resposta como texto
    """

    separador = b"\r\n\r\n"
    pos = dados.find(separador)

    if pos == -1:
        return ""

    return dados[pos + len(separador):].decode("utf-8", errors="replace")


def conectar_com_certificado_proprio(host: str, porta: int, cert: str) -> Dict:
    """
    Conecta ao servidor TLS usando o certificado self-signed como âncora de confiança explícita

    Args:
        host (str): Endereço do servidor
        porta (int): Porta TLS do servidor
        cert (str): Caminho para o arquivo .crt usado como âncora de confiança

    Returns:
        Dict: Dicionário com versão TLS, cipher, status, headers, corpo e dados brutos
    """

    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    contexto.load_verify_locations(cafile=cert)
    contexto.minimum_version = ssl.TLSVersion.TLSv1_2

    try:
        with socket.create_connection((host, porta), timeout=10) as sock_raw:
            with contexto.wrap_socket(sock_raw, server_hostname=host) as sock_tls:
                versao = sock_tls.version()
                cipher = sock_tls.cipher()

                sock_tls.sendall(montar_requisicao("/", host))

                dados = b""

                while True:
                    fragmento = sock_tls.recv(TAMANHO_BUFFER)

                    if not fragmento:
                        break

                    dados += fragmento

                return {
                    "erro": None,
                    "versao": versao,
                    "cipher": cipher,
                    "status": extrair_status(dados),
                    "headers": extrair_headers(dados),
                    "corpo": extrair_corpo(dados),
                }

    except ssl.SSLCertVerificationError as e:
        return {"erro": f"Falha na verificação do certificado: {e}"}

    except ssl.SSLError as e:
        return {"erro": f"Erro TLS: {e}"}

    except (socket.timeout, TimeoutError):
        return {"erro": "Timeout ao conectar"}

    except OSError as e:
        return {"erro": f"Erro de socket: {e}"}


def exibir_resultado(resultado: Dict) -> None:
    """
    Imprime no terminal as informações da sessão TLS e o conteúdo da resposta recebida

    Args:
        resultado (Dict): Dicionário retornado por conectar_com_certificado_proprio
    """

    print(f"\n{'=' * 100}")
    print("RESULTADO DA CONEXÃO TLS COM CERTIFICADO SELF-SIGNED")
    print(f"{'=' * 100}\n")

    if resultado.get("erro"):
        print(f"  ERRO: {resultado['erro']}\n")
        return

    cipher = resultado["cipher"]

    print("  SESSÃO TLS")
    print(f"    Versão: {resultado['versao']}")
    print(f"    Cipher: {cipher[0] if cipher else '-'}")
    print(f"    Protocolo: {cipher[1] if cipher else '-'}")
    print(f"    Bits: {cipher[2] if cipher else '-'}")

    print()
    print("  STATUS HTTP")
    print(f"    {resultado['status']}")

    print()
    print("  HEADERS")

    for chave, valor in resultado["headers"].items():
        print(f"    {chave}: {valor}")

    print()
    print("  PAYLOAD")

    for linha in resultado["corpo"].splitlines():
        print(f"    {linha}")

    print()


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


registrar(f"Conectando a {HOST_SERVIDOR}:{PORTA} com certificado {ARQUIVO_CERT} como âncora")
resultado = conectar_com_certificado_proprio(HOST_SERVIDOR, PORTA, ARQUIVO_CERT)
exibir_resultado(resultado)
exibir_log()
