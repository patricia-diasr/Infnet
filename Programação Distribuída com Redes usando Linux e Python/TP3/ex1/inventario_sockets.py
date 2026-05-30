import socket
import datetime
from typing import List, Dict


PORTA = 12345
HOST_IPV4 = "127.0.0.1"
HOST_IPV6 = "::1"

CONFIGURACOES = [
    {
        "familia": socket.AF_INET,
        "tipo": socket.SOCK_STREAM,
        "host": HOST_IPV4,
        "rotulo": "AF_INET + SOCK_STREAM (TCP IPv4)",
    },
    {
        "familia": socket.AF_INET,
        "tipo": socket.SOCK_DGRAM,
        "host": HOST_IPV4,
        "rotulo": "AF_INET + SOCK_DGRAM  (UDP IPv4)",
    },
    {
        "familia": socket.AF_INET6,
        "tipo": socket.SOCK_STREAM,
        "host": HOST_IPV6,
        "rotulo": "AF_INET6 + SOCK_STREAM (TCP IPv6)",
    },
    {
        "familia": socket.AF_INET6,
        "tipo": socket.SOCK_DGRAM,
        "host": HOST_IPV6,
        "rotulo": "AF_INET6 + SOCK_DGRAM (UDP IPv6)",
    },
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


def criar_e_vincular_socket(familia: socket.AddressFamily, tipo: socket.SocketKind, host: str, porta: int) -> Dict:
    """
    Cria um socket com a família e tipo fornecidos, vincula ao endereço indicado e o encerra corretamente

    Args:
        familia (socket.AddressFamily): Família de endereços, AF_INET ou AF_INET6
        tipo (socket.SocketKind): Tipo do socket, SOCK_STREAM ou SOCK_DGRAM
        host (str): Endereço de escuta
        porta (int): Porta de escuta

    Returns:
        Dict: Dicionário com os campos 'sucesso' (bool) e 'erro' (str ou None)
    """

    sock = None

    try:
        sock = socket.socket(familia, tipo)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, porta))

        if tipo == socket.SOCK_STREAM:
            sock.listen(1)

        return {"sucesso": True, "erro": None}

    except OSError as e:
        return {"sucesso": False, "erro": str(e)}

    finally:
        if sock is not None:
            sock.close()


def executar_inventario() -> List[Dict]:
    """
    Percorre todas as configurações definidas, executa a criação e vinculação de cada socket e coleta os resultados

    Returns:
        List[Dict]: Lista de dicionários com os campos 'rotulo', 'sucesso' e 'erro'
    """

    resultados = []

    for cfg in CONFIGURACOES:
        registrar(f"Testando: {cfg['rotulo']}")
        resultado = criar_e_vincular_socket(cfg["familia"], cfg["tipo"], cfg["host"], PORTA)
        resultado["rotulo"] = cfg["rotulo"]

        if resultado["sucesso"]:
            registrar(f"  Resultado: sucesso")

        else:
            registrar(f"  Resultado: erro ({resultado['erro']})")

        resultados.append(resultado)

    return resultados


def exibir_tabela(resultados: List[Dict]) -> None:
    """
    Exibe os resultados do inventário em formato tabular

    Args:
        resultados (List[Dict]): Lista de resultados retornada por executar_inventario
    """

    col_n = 4
    col_rotulo = 42
    col_status = 10
    col_erro = 40

    sep = f"+{'-' * (col_n + 2)}+{'-' * (col_rotulo + 2)}+{'-' * (col_status + 2)}+{'-' * (col_erro + 2)}+"
    cab = (f"| {'#':^{col_n}} | {'Configuração':^{col_rotulo}} | {'Status':^{col_status}} | {'Erro':^{col_erro}} |")

    print(f"\n{'=' * 100}")
    print("INVENTÁRIO DE SOCKETS")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for i, r in enumerate(resultados, 1):
        status = "OK" if r["sucesso"] else "ERRO"
        erro = r["erro"] if r["erro"] else "-"

        if len(erro) > col_erro:
            erro = erro[:col_erro - 3] + "..."

        print(f"| {str(i):^{col_n}} | {r['rotulo']:<{col_rotulo}} | {status:^{col_status}} | {erro:<{col_erro}} |")

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


resultados = executar_inventario()
exibir_tabela(resultados)
exibir_log()
