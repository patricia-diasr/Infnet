import socket
import struct
import time
from typing import List, Tuple


HOST_SERVIDOR = "192.168.56.101"
PORTA = 9000
TAMANHO_CABECALHO = 4


def criar_mensagem(conteudo: str, tamanho_declarado: int = -1) -> bytes:
    """
    Serializa uma mensagem no protocolo tamanho mais conteúdo

    Args:
        conteudo (str): Texto a enviar como corpo da mensagem
        tamanho_declarado (int): Tamanho a declarar no cabeçalho. Quando -1, usa o tamanho real do conteúdo

    Returns:
        bytes: Mensagem serializada com cabeçalho de tamanho prefixado
    """

    corpo = conteudo.encode("utf-8")
    tamanho = len(corpo) if tamanho_declarado == -1 else tamanho_declarado
    cabecalho = struct.pack("!I", tamanho)
    return cabecalho + corpo


def receber_resposta(sock: socket.socket) -> str:
    """
    Recebe e decodifica a resposta estruturada enviada pelo servidor

    Args:
        sock (socket.socket): Socket da conexão ativa com o servidor

    Returns:
        str: Texto da resposta decodificada ou mensagem de erro em caso de falha
    """

    cabecalho = sock.recv(TAMANHO_CABECALHO)

    if not cabecalho or len(cabecalho) < TAMANHO_CABECALHO:
        return "Resposta inválida ou conexão encerrada"

    tamanho = struct.unpack("!I", cabecalho)[0]
    corpo = sock.recv(tamanho)
    return corpo.decode("utf-8", errors="replace")


def exibir_envio(numero: int, descricao: str, conteudo: str, tamanho_declarado: int, resposta: str) -> None:
    """
    Exibe no terminal os detalhes de um envio e a resposta recebida do servidor

    Args:
        numero (int): Número sequencial da mensagem enviada
        descricao (str): Descrição do tipo de mensagem enviada
        conteudo (str): Texto do conteúdo enviado
        tamanho_declarado (int): Tamanho declarado no cabeçalho da mensagem
        resposta (str): Texto da resposta recebida do servidor
    """

    tamanho_real = len(conteudo.encode("utf-8"))

    print(f"\n  Mensagem {numero}: {descricao}")
    print(f"    Conteúdo: {conteudo}")
    print(f"    Tamanho real: {tamanho_real} bytes")
    print(f"    Tamanho declarado: {tamanho_declarado} bytes")
    print(f"    Resposta do servidor: {resposta}")


def executar_cliente(host: str, porta: int) -> None:
    """
    Conecta ao servidor TCP e envia uma sequência de mensagens com e sem inconsistência de framing

    Args:
        host (str): Endereço IP do servidor
        porta (int): Porta do servidor
    """

    mensagens: List[Tuple[str, str, int]] = [
        ("Mensagem válida", "Olá, servidor", -1),
        ("Mensagem com tamanho subdeclarado", "Mensagem longa com muitos bytes", 5),
        ("Mensagem válida", "Outra mensagem correta", -1),
        ("Mensagem com tamanho superdeclarado", "Curta", 50),
    ]

    print(f"\n{'=' * 60}")
    print("CLIENTE TCP COM FRAMING")
    print(f"{'=' * 60}")
    print(f"\n  Conectando em {host}:{porta}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, porta))
        print(f"  Conexão estabelecida\n")

        for i, (descricao, conteudo, tamanho_declarado) in enumerate(mensagens, 1):
            corpo = conteudo.encode("utf-8")
            tamanho_real = len(corpo)
            tamanho_usado = tamanho_real if tamanho_declarado == -1 else tamanho_declarado

            mensagem = criar_mensagem(conteudo, tamanho_declarado)
            sock.sendall(mensagem)

            time.sleep(0.3)

            resposta = receber_resposta(sock)
            exibir_envio(i, descricao, conteudo, tamanho_usado, resposta)

    print(f"\n  Todas as mensagens enviadas. Conexão encerrada.\n")


executar_cliente(HOST_SERVIDOR, PORTA)
