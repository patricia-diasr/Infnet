import socket
import datetime
import struct
import os


HOST_SERVIDOR = "192.168.56.101"
PORTA = 55000

ARQUIVO_ENVIAR = "arquivo_teste.txt"

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


def criar_arquivo_teste(caminho: str) -> None:
    """
    Cria um arquivo de texto de exemplo caso ele ainda não exista no disco

    Args:
        caminho (str): Caminho do arquivo a criar
    """

    if os.path.exists(caminho):
        return

    conteudo = (
        "Linha 1: conteúdo de teste para transferência via TCP\n"
        "Linha 2: demonstração de envio em três chamadas send\n"
        "Linha 3: nome, tamanho e conteúdo enviados separadamente\n"
        "Linha 4: servidor reagrupa os fragmentos e salva o arquivo\n"
        "Linha 5: fim do arquivo de teste\n"
    )

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    registrar(f"Arquivo de teste criado: {caminho}")


def ler_arquivo(caminho: str) -> tuple:
    """
    Lê o arquivo do disco e retorna nome, tamanho e conteúdo em bytes

    Args:
        caminho (str): Caminho do arquivo a ler

    Returns:
        tuple: Tupla com (nome_arquivo, tamanho_bytes, conteudo_bytes)
    """

    nome = os.path.basename(caminho)
    tamanho = os.path.getsize(caminho)

    with open(caminho, "rb") as arquivo:
        conteudo = arquivo.read()

    return nome, tamanho, conteudo


def exibir_arquivo_original(nome: str, tamanho: int, conteudo: bytes) -> None:
    """
    Imprime no terminal o nome, tamanho e conteúdo do arquivo original antes do envio

    Args:
        nome (str): Nome do arquivo
        tamanho (int): Tamanho em bytes do arquivo
        conteudo (bytes): Conteúdo bruto do arquivo
    """

    print(f"\n{'=' * 100}")
    print("  ARQUIVO ORIGINAL")
    print(f"{'=' * 100}\n")
    print(f"  Nome: {nome}")
    print(f"  Tamanho: {tamanho} bytes")
    print(f"\n  CONTEÚDO:\n")

    try:
        texto = conteudo.decode("utf-8")

        for linha in texto.splitlines():
            print(f"    {linha}")

    except UnicodeDecodeError:
        print(f"    (conteúdo binário, {tamanho} bytes, não exibível como texto)")

    print()


def enviar_arquivo(sock: socket.socket, nome: str, tamanho: int, conteudo: bytes) -> None:
    """
    Envia o arquivo ao servidor em exatamente três chamadas send, cada uma precedida por um cabeçalho de tamanho

    Args:
        sock (socket.socket): Socket com conexão ativa
        nome (str): Nome do arquivo a enviar
        tamanho (int): Tamanho em bytes do conteúdo
        conteudo (bytes): Bytes do conteúdo do arquivo
    """

    registrar("  Send 1: enviando nome do arquivo")
    nome_bytes = nome.encode("utf-8")
    cabecalho_nome = struct.pack("!I", len(nome_bytes))
    sock.send(cabecalho_nome + nome_bytes)
    registrar(f"  Nome enviado: '{nome}' ({len(nome_bytes)} bytes de payload + 4 de cabeçalho)")

    registrar("  Send 2: enviando tamanho do arquivo")
    tamanho_bytes = struct.pack("!Q", tamanho)
    sock.send(tamanho_bytes)
    registrar(f"  Tamanho enviado: {tamanho} bytes (8 bytes no wire)")

    registrar("  Send 3: enviando conteúdo do arquivo")
    sock.send(conteudo)
    registrar(f"  Conteúdo enviado: {len(conteudo)} bytes")


def executar_cliente() -> None:
    """
    Cria o arquivo de teste se necessário, lê do disco, exibe os dados e envia ao servidor em três chamadas send
    """

    criar_arquivo_teste(ARQUIVO_ENVIAR)

    try:
        nome, tamanho, conteudo = ler_arquivo(ARQUIVO_ENVIAR)
    except OSError as e:
        registrar(f"Erro ao ler arquivo '{ARQUIVO_ENVIAR}': {e}")
        exibir_log()
        return

    exibir_arquivo_original(nome, tamanho, conteudo)

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST_SERVIDOR, PORTA))

        registrar(f"Conexão estabelecida com {HOST_SERVIDOR}:{PORTA}")
        registrar(f"Endereço local: {sock.getsockname()[0]}:{sock.getsockname()[1]}")

        enviar_arquivo(sock, nome, tamanho, conteudo)

        registrar("Envio concluído com sucesso")

    except ConnectionRefusedError:
        registrar(f"Erro: conexão recusada em {HOST_SERVIDOR}:{PORTA}")

    except OSError as e:
        registrar(f"Erro de socket: {e}")

    finally:
        if sock:
            sock.close()
            registrar("Socket encerrado")

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
