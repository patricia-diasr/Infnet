import socket
import datetime
import sys
from typing import Dict, List, Tuple


HOST_SERVIDOR = "127.0.0.1"
PORTA = 8080

TAMANHO_BUFFER = 4096

CAMINHOS_TESTE: List[str] = ["/", "/health", "/nao-existe"]

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


def receber_resposta_completa(sock: socket.socket) -> bytes:
    """
    Lê todos os bytes da resposta até o servidor encerrar a conexão

    Args:
        sock (socket.socket): Socket com a conexão já estabelecida

    Returns:
        bytes: Bytes completos da resposta HTTP
    """

    dados = b""

    while True:
        fragmento = sock.recv(TAMANHO_BUFFER)

        if not fragmento:
            break

        dados += fragmento

    return dados


def dissecar_resposta(dados: bytes) -> Tuple[str, Dict[str, str], str]:
    """
    Separa e interpreta status line, headers e corpo da resposta HTTP

    Args:
        dados (bytes): Bytes brutos da resposta HTTP recebida

    Returns:
        Tuple[str, Dict[str, str], str]: Status line, dicionário de headers e corpo como texto
    """

    try:
        separador = b"\r\n\r\n"
        pos = dados.find(separador)

        if pos == -1:
            return "(sem status)", {}, dados.decode("utf-8", errors="replace")

        cabecalho_bruto = dados[:pos].decode("utf-8", errors="replace")
        corpo_bruto = dados[pos + len(separador):]

        linhas = cabecalho_bruto.splitlines()
        status_line = linhas[0] if linhas else "(vazio)"
        headers = {}

        for linha in linhas[1:]:
            if ":" in linha:
                chave, _, valor = linha.partition(":")
                headers[chave.strip()] = valor.strip()

        corpo = corpo_bruto.decode("utf-8", errors="replace")

        return status_line, headers, corpo

    except Exception as e:
        return f"(erro ao dissecar: {e})", {}, ""


def exibir_resposta(numero: int, caminho: str, status: str, headers: Dict[str, str], corpo: str) -> None:
    """
    Imprime no terminal o status, headers e payload de forma estruturada

    Args:
        numero (int): Número sequencial do teste
        caminho (str): Caminho requisitado
        status (str): Status line extraída da resposta
        headers (Dict[str, str]): Cabeçalhos HTTP recebidos
        corpo (str): Corpo da resposta
    """

    print(f"\n{'=' * 100}")
    print(f"Requisição {numero}: GET {caminho}")
    print(f"{'=' * 100}\n")

    print(f"  STATUS")
    print(f"    {status}\n")

    print(f"  HEADERS")
    for chave, valor in headers.items():
        print(f"    {chave}: {valor}")

    print(f"\n  PAYLOAD")
    for linha in corpo.splitlines():
        print(f"    {linha}")

    print()


def executar_cliente() -> None:
    """
    Percorre todos os caminhos de teste, envia requisições GET e exibe as respostas dissecadas
    """

    for numero, caminho in enumerate(CAMINHOS_TESTE, 1):
        registrar(f"Requisitando GET {caminho}")
        sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST_SERVIDOR, PORTA))

            requisicao = montar_requisicao(caminho, HOST_SERVIDOR)
            sock.sendall(requisicao)

            dados = receber_resposta_completa(sock)
            status, headers, corpo = dissecar_resposta(dados)

            registrar(f"  Resposta recebida: {status}  ({len(dados)} bytes no total)")
            exibir_resposta(numero, caminho, status, headers, corpo)

        except ConnectionRefusedError:
            registrar(f"  Erro: conexão recusada em {HOST_SERVIDOR}:{PORTA}")

        except OSError as e:
            registrar(f"  Erro de socket: {e}")

        finally:
            if sock:
                sock.close()

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


executar_cliente()
