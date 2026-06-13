import socket
import struct
from typing import Tuple, Optional


HOST = "0.0.0.0"
PORTA = 9000
TAMANHO_CABECALHO = 4
TIMEOUT_LEITURA = 0.2
TAMANHO_MAX_EXTRA = 65536


def criar_socket_servidor(host: str, porta: int) -> socket.socket:
    """
    Cria e configura o socket TCP do servidor pronto para aceitar conexões

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


def receber_exatamente(conn: socket.socket, n_bytes: int) -> Optional[bytes]:
    """
    Recebe exatamente n_bytes do socket, reagrupando fragmentos TCP se necessário

    Args:
        conn (socket.socket): Socket da conexão ativa
        n_bytes (int): Quantidade exata de bytes a receber

    Returns:
        Optional[bytes]: Bytes recebidos ou None se a conexão foi encerrada
    """

    buffer = b""

    while len(buffer) < n_bytes:
        fragmento = conn.recv(n_bytes - len(buffer))

        if not fragmento:
            return None

        buffer += fragmento

    return buffer


def receber_com_timeout(conn: socket.socket, n_bytes: int, tempo_limite: float) -> bytes:
    """
    Recebe até n_bytes do socket, interrompendo a leitura caso nenhum dado novo chegue dentro do tempo limite

    Args:
        conn (socket.socket): Socket da conexão ativa
        n_bytes (int): Quantidade máxima de bytes a receber
        tempo_limite (float): Tempo em segundos de espera por novos dados antes de desistir

    Returns:
        bytes: Bytes efetivamente recebidos, podendo ser menor que n_bytes
    """

    buffer = b""
    conn.settimeout(tempo_limite)

    try:
        while len(buffer) < n_bytes:
            fragmento = conn.recv(n_bytes - len(buffer))

            if not fragmento:
                break

            buffer += fragmento

    except socket.timeout:
        pass

    finally:
        conn.settimeout(None)

    return buffer


def ler_mensagem(conn: socket.socket) -> Tuple[Optional[int], Optional[bytes]]:
    """
    Lê uma mensagem completa do socket seguindo o protocolo tamanho mais conteúdo

    Args:
        conn (socket.socket): Socket da conexão ativa

    Returns:
        Tuple[Optional[int], Optional[bytes]]: (tamanho declarado no cabeçalho, bytes do conteúdo recebido)
        Retorna (None, None) se a conexão foi encerrada pelo cliente antes do cabeçalho
    """

    cabecalho = receber_exatamente(conn, TAMANHO_CABECALHO)

    if cabecalho is None:
        return None, None

    tamanho_declarado = struct.unpack("!I", cabecalho)[0]
    conteudo = receber_com_timeout(conn, tamanho_declarado, TIMEOUT_LEITURA)
    extra = receber_com_timeout(conn, TAMANHO_MAX_EXTRA, TIMEOUT_LEITURA)
    conteudo += extra

    return tamanho_declarado, conteudo


def construir_resposta(status: str, detalhe: str) -> bytes:
    """
    Constrói uma resposta estruturada no formato tamanho mais conteúdo para enviar ao cliente

    Args:
        status (str): Indicador do resultado, como "OK" ou "ERRO"
        detalhe (str): Mensagem descritiva do resultado

    Returns:
        bytes: Resposta serializada com cabeçalho de tamanho prefixado
    """

    corpo = f"{status}|{detalhe}".encode("utf-8")
    cabecalho = struct.pack("!I", len(corpo))
    return cabecalho + corpo


def processar_mensagem(tamanho_declarado: int, conteudo: bytes) -> bytes:
    """
    Valida a consistência entre o tamanho declarado e o conteúdo recebido e produz a resposta adequada

    Args:
        tamanho_declarado (int): Tamanho em bytes declarado no cabeçalho da mensagem
        conteudo (bytes): Bytes efetivamente recebidos como corpo da mensagem

    Returns:
        bytes: Resposta serializada a ser enviada ao cliente
    """

    tamanho_recebido = len(conteudo)

    print(f"\n  Mensagem recebida:")
    print(f"    Tamanho declarado: {tamanho_declarado} bytes")
    print(f"    Tamanho recebido: {tamanho_recebido} bytes")
    print(f"    Conteúdo: {conteudo.decode('utf-8', errors='replace')}")

    if tamanho_declarado != tamanho_recebido:
        detalhe = f"inconsistência: declarado {tamanho_declarado} bytes, recebido {tamanho_recebido} bytes"
        print(f"    Validação: ERRO ({detalhe})")
        return construir_resposta("ERRO", detalhe)

    print(f"    Validação: OK")
    return construir_resposta("OK", f"mensagem de {tamanho_recebido} bytes recebida com sucesso")


def atender_conexao(conn: socket.socket, endereco: Tuple[str, int]) -> None:
    """
    Gerencia o ciclo completo de uma conexão TCP, lendo e respondendo múltiplas mensagens

    Args:
        conn (socket.socket): Socket da conexão ativa com o cliente
        endereco (Tuple[str, int]): Endereço IP e porta do cliente conectado
    """

    print(f"\n  Conexão aceita de {endereco[0]}:{endereco[1]}")

    with conn:
        while True:
            tamanho_declarado, conteudo = ler_mensagem(conn)

            if tamanho_declarado is None:
                print(f"  Conexão encerrada pelo cliente {endereco[0]}:{endereco[1]}")
                break

            resposta = processar_mensagem(tamanho_declarado, conteudo)
            conn.sendall(resposta)


def executar_servidor(host: str, porta: int) -> None:
    """
    Inicializa o servidor TCP e entra em loop aguardando conexões sequenciais

    Args:
        host (str): Endereço de escuta do servidor
        porta (int): Porta de escuta do servidor
    """

    sock = criar_socket_servidor(host, porta)

    print(f"\n{'=' * 60}")
    print("SERVIDOR TCP COM FRAMING")
    print(f"{'=' * 60}")
    print(f"\n  Aguardando conexões em {host}:{porta}")

    while True:
        conn, endereco = sock.accept()
        atender_conexao(conn, endereco)


executar_servidor(HOST, PORTA)
