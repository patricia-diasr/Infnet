import socket
import datetime
import time
from typing import List, Dict, Tuple


HOST_SERVIDOR = "::1"
PORTA = 12346

TAMANHO_BUFFER = 4096
TIMEOUT = 5.0

MENSAGENS_TESTE: List[str] = [
    "Primeira mensagem via IPv6",
    "Segunda mensagem com caracteres especiais: áéíóú",
    "Terceira mensagem com payload maior: " + ("X" * 64),
]

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


def exibir_info_socket(sock: socket.socket) -> None:
    """
    Exibe as informações do socket criado, incluindo família, tipo e endereço local

    Args:
        sock (socket.socket): Socket a inspecionar
    """

    nome_local = sock.getsockname()

    registrar(f"  Família: {sock.family.name}")
    registrar(f"  Tipo: {sock.type.name}")
    registrar(f"  Endereço local: [{nome_local[0]}]:{nome_local[1]}")
    registrar(f"  Flow info: {nome_local[2]}")
    registrar(f"  Scope ID: {nome_local[3]}")


def verificar_suporte_ipv6() -> bool:
    """
    Verifica se o sistema operacional suporta IPv6 tentando criar um socket AF_INET6

    Returns:
        bool: True se IPv6 estiver disponível, False caso contrário
    """

    try:
        sock_teste = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock_teste.close()
        registrar("Suporte a IPv6 disponível no sistema operacional")
        return True

    except OSError as e:
        registrar(f"IPv6 não disponível no sistema operacional: {e}")
        return False


def receber_banner(sock: socket.socket) -> str:
    """
    Aguarda e retorna o banner inicial enviado pelo servidor

    Args:
        sock (socket.socket): Socket com conexão já estabelecida

    Returns:
        str: Texto do banner recebido
    """

    try:
        dados = sock.recv(TAMANHO_BUFFER)
        return dados.decode("utf-8", errors="replace")

    except socket.timeout:
        return "(banner não recebido dentro do timeout)"


def enviar_e_receber(sock: socket.socket, mensagem: str) -> Tuple[bool, str, float]:
    """
    Envia uma mensagem ao servidor e aguarda o echo, medindo a latência

    Args:
        sock (socket.socket): Socket com conexão ativa
        mensagem (str): Mensagem a enviar

    Returns:
        Tuple[bool, str, float]: Sucesso do recebimento, texto do echo e latência em ms
    """

    payload = mensagem.encode("utf-8")

    try:
        t_inicio = time.perf_counter()
        sock.sendall(payload)

        echo = sock.recv(TAMANHO_BUFFER)
        t_fim = time.perf_counter()

        latencia = (t_fim - t_inicio) * 1000
        texto_echo = echo.decode("utf-8", errors="replace").strip()

        return True, texto_echo, round(latencia, 2)

    except socket.timeout:
        return False, "(timeout)", 0.0

    except OSError as e:
        return False, f"(erro: {e})", 0.0


def executar_cliente() -> List[Dict]:
    """
    Verifica suporte a IPv6, conecta ao servidor, exibe informações do socket e executa os envios de teste

    Returns:
        List[Dict]: Lista de resultados com os dados de cada envio
    """

    if not verificar_suporte_ipv6():
        registrar("Abortando: cliente IPv6 não pode ser iniciado sem suporte do sistema")
        exibir_log()
        return []

    resultados = []
    sock = None

    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        registrar(f"Conectando a [{HOST_SERVIDOR}]:{PORTA}")
        sock.connect((HOST_SERVIDOR, PORTA, 0, 0))

        registrar("Conexão TCP IPv6 estabelecida")
        exibir_info_socket(sock)

        banner = receber_banner(sock)
        registrar(f"Banner recebido ({len(banner)} bytes)")

        print()
        print("  BANNER DO SERVIDOR:")

        for linha in banner.strip().splitlines():
            print(f"    {linha}")

        print()

        for i, mensagem in enumerate(MENSAGENS_TESTE, 1):
            registrar(f"Enviando mensagem {i}: '{mensagem[:50]}{'...' if len(mensagem) > 50 else ''}'")

            sucesso, echo, latencia = enviar_e_receber(sock, mensagem)

            registrar(f"  Echo recebido: {'sim' if sucesso else 'não'}")
            registrar(f"  Íntegro: {'sim' if sucesso and echo == mensagem else 'não'}")
            registrar(f"  Latência: {latencia} ms")

            resultados.append({
                "id": i,
                "mensagem": mensagem[:60],
                "bytes": len(mensagem.encode("utf-8")),
                "sucesso": sucesso,
                "integro": sucesso and echo == mensagem,
                "latencia_ms": latencia,
            })

        registrar("Enviando comando de encerramento")
        sock.sendall("sair\n".encode("utf-8"))
        time.sleep(0.3)

    except ConnectionRefusedError:
        registrar(f"Erro: conexão recusada em [{HOST_SERVIDOR}]:{PORTA}")

    except socket.timeout:
        registrar("Erro: timeout ao tentar conectar")

    except OSError as e:
        registrar(f"Erro de socket: {e}")

    finally:
        if sock:
            sock.close()
            registrar("Socket encerrado")

    return resultados


def exibir_tabela(resultados: List[Dict]) -> None:
    """
    Exibe os resultados dos envios em formato tabular

    Args:
        resultados (List[Dict]): Lista retornada por executar_cliente
    """

    if not resultados:
        return

    col_id = 4
    col_msg = 60
    col_bytes = 6
    col_suc = 6
    col_int = 8
    col_lat = 14

    sep = (f"+{'-' * (col_id + 2)}+{'-' * (col_msg + 2)}+{'-' * (col_bytes + 2)}+{'-' * (col_suc + 2)}+{'-' * (col_int + 2)}+{'-' * (col_lat + 2)}+")
    cab = (f"| {'#':^{col_id}} | {'Mensagem (resumida)':^{col_msg}} | {'Bytes':^{col_bytes}} | {'Echo':^{col_suc}} | {'Íntegro':^{col_int}} | {'Latência (ms)':^{col_lat}} |")

    print(f"\n{'=' * 100}")
    print("RESULTADOS DO CLIENTE TCP IPv6")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        suc = "Sim" if r["sucesso"] else "Não"
        ing = "Sim" if r["integro"]  else "Não"
        lat = f"{r['latencia_ms']:.2f}"
        print(f"| {str(r['id']):^{col_id}} | {r['mensagem']:<{col_msg}} | {str(r['bytes']):^{col_bytes}} | {suc:^{col_suc}} | {ing:^{col_int}} | {lat:^{col_lat}} |")

    print(sep)


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


resultados = executar_cliente()
exibir_tabela(resultados)
exibir_log()
