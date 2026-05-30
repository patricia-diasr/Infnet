import socket
import datetime
import struct


HOST = "0.0.0.0"
PORTA = 55000

TAMANHO_BUFFER = 4096
PREFIXO_SALVO = "recebido_"

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


def receber_exato(conexao: socket.socket, quantidade: int) -> bytes:
    """
    Lê exatamente a quantidade de bytes solicitada do socket, reagrupando fragmentos se necessário

    Args:
        conexao (socket.socket): Socket com conexão ativa
        quantidade (int): Número exato de bytes a receber

    Returns:
        bytes: Exatamente quantidade bytes lidos do socket
    """

    dados = b""

    while len(dados) < quantidade:
        fragmento = conexao.recv(min(TAMANHO_BUFFER, quantidade - len(dados)))

        if not fragmento:
            break

        dados += fragmento

    return dados


def receber_campo_texto(conexao: socket.socket) -> str:
    """
    Recebe um campo de texto precedido por um inteiro de 4 bytes indicando seu tamanho

    Args:
        conexao (socket.socket): Socket com conexão ativa

    Returns:
        str: Texto decodificado recebido do cliente
    """

    tamanho_bruto = receber_exato(conexao, 4)
    tamanho = struct.unpack("!I", tamanho_bruto)[0]
    dados = receber_exato(conexao, tamanho)
    return dados.decode("utf-8")


def receber_arquivo(conexao: socket.socket) -> tuple:
    """
    Recebe o nome, tamanho e conteúdo do arquivo em três etapas distintas via socket

    Args:
        conexao (socket.socket): Socket com conexão ativa

    Returns:
        tuple: Tupla com (nome_arquivo, tamanho_declarado, conteudo_bytes)
    """

    registrar("  Etapa 1: recebendo nome do arquivo")
    nome = receber_campo_texto(conexao)
    registrar(f"  Nome recebido: {nome}")

    registrar("  Etapa 2: recebendo tamanho do arquivo")
    tamanho_bruto = receber_exato(conexao, 8)
    tamanho_declarado = struct.unpack("!Q", tamanho_bruto)[0]
    registrar(f"  Tamanho declarado: {tamanho_declarado} bytes")

    registrar("  Etapa 3: recebendo conteúdo do arquivo")
    conteudo = receber_exato(conexao, tamanho_declarado)
    registrar(f"  Conteúdo recebido: {len(conteudo)} bytes")

    return nome, tamanho_declarado, conteudo


def salvar_arquivo(nome_original: str, conteudo: bytes) -> str:
    """
    Salva o conteúdo recebido em disco com um nome diferente do original

    Args:
        nome_original (str): Nome original do arquivo enviado pelo cliente
        conteudo (bytes): Bytes do conteúdo a salvar

    Returns:
        str: Caminho do arquivo salvo
    """

    nome_salvo = PREFIXO_SALVO + nome_original

    with open(nome_salvo, "wb") as arquivo:
        arquivo.write(conteudo)

    return nome_salvo


def exibir_arquivo_recebido(nome: str, tamanho_declarado: int, conteudo: bytes, nome_salvo: str) -> None:
    """
    Imprime no terminal as informações e o conteúdo do arquivo recebido

    Args:
        nome_declarado (str): Nome do arquivo informado pelo cliente
        tamanho_declarado (int): Tamanho em bytes declarado pelo cliente
        conteudo (bytes): Bytes do conteúdo recebido
        nome_salvo (str): Nome com que o arquivo foi salvo localmente
    """

    print(f"\n{'=' * 100}")
    print("ARQUIVO RECEBIDO")
    print(f"{'=' * 100}\n")
    print(f"  Nome original: {nome}")
    print(f"  Tamanho declarado: {tamanho_declarado} bytes")
    print(f"  Bytes recebidos: {len(conteudo)}")
    print(f"  Íntegro: {'sim' if len(conteudo) == tamanho_declarado else 'não'}")
    print(f"  Salvo como: {nome_salvo}")
    print(f"\n  CONTEÚDO:\n")

    try:
        texto = conteudo.decode("utf-8")

        for linha in texto.splitlines():
            print(f"    {linha}")

    except UnicodeDecodeError:
        print(f"    (conteúdo binário, {len(conteudo)} bytes, não exibível como texto)")

    print()


def atender_cliente(conexao: socket.socket, endereco: tuple) -> None:
    """
    Gerencia o recebimento completo do arquivo de um cliente conectado

    Args:
        conexao (socket.socket): Socket da conexão estabelecida
        endereco (tuple): IP e porta do cliente
    """

    registrar(f"Conexão recebida de {endereco[0]}:{endereco[1]}")

    try:
        nome, tamanho_declarado, conteudo = receber_arquivo(conexao)
        nome_salvo = salvar_arquivo(nome, conteudo)
        exibir_arquivo_recebido(nome, tamanho_declarado, conteudo, nome_salvo)
        registrar(f"Arquivo '{nome}' recebido e salvo como '{nome_salvo}'")

    except (ConnectionResetError, BrokenPipeError):
        registrar(f"Conexão encerrada abruptamente por {endereco[0]}")

    except struct.error as e:
        registrar(f"Erro ao interpretar cabeçalho do protocolo: {e}")

    except OSError as e:
        registrar(f"Erro ao salvar arquivo: {e}")

    finally:
        conexao.close()
        registrar(f"Conexão encerrada com {endereco[0]}:{endereco[1]}")


def iniciar_servidor() -> None:
    """
    Inicializa o servidor TCP, aguarda uma conexão, recebe o arquivo e encerra
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORTA))
        sock.listen(1)

        registrar(f"Servidor aguardando conexão em {HOST}:{PORTA}")

        conexao, endereco = sock.accept()
        atender_cliente(conexao, endereco)

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
