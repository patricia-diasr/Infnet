import socket
import datetime
import time
import errno
from typing import List, Dict


HOST_ALVO = "127.0.0.1"

ALVOS: List[Dict] = [
    {
        "host": HOST_ALVO,
        "porta": 22,
        "rotulo": "SSH (porta conhecida do sistema)",
        "categoria": "sistema",
    },
    {
        "host": HOST_ALVO,
        "porta": 80,
        "rotulo": "HTTP (porta conhecida do sistema)",
        "categoria": "sistema",
    },
    {
        "host": HOST_ALVO,
        "porta": 12345,
        "rotulo": "Porta aberta (servidor do exercício 3)",
        "categoria": "aberta",
    },
    {
        "host": HOST_ALVO,
        "porta": 19999,
        "rotulo": "Porta fechada (sem serviço)",
        "categoria": "fechada",
    },
    {
        "host": HOST_ALVO,
        "porta": 39999,
        "rotulo": "Porta fechada (sem serviço)",
        "categoria": "fechada",
    },
]

TIMEOUT_CONEXAO = 3.0

TABELA_ERRNO: Dict[int, str] = {
    0: "Conexão estabelecida com sucesso",
    errno.ECONNREFUSED: "Conexão recusada (porta fechada ou sem serviço)",
    errno.ETIMEDOUT: "Timeout (host inacessível ou filtrado por firewall)",
    errno.ENETUNREACH: "Rede inacessível (rota inexistente)",
    errno.EHOSTUNREACH: "Host inacessível (sem rota até o destino)",
    errno.EACCES: "Permissão negada (porta privilegiada sem root)",
    errno.EADDRINUSE: "Endereço já em uso",
}

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


def interpretar_codigo(codigo: int) -> str:
    """
    Retorna a descrição associada ao código errno retornado por connect_ex

    Args:
        codigo (int): Código de retorno de connect_ex

    Returns:
        str: Descrição legível do código, ou mensagem genérica para códigos desconhecidos
    """

    return TABELA_ERRNO.get(codigo, f"Código errno {codigo}: {errno.errorcode.get(codigo, 'desconhecido')}")


def inferir_estado(codigo: int) -> str:
    """
    Infere o estado da porta a partir do código errno retornado por connect_ex

    Args:
        codigo (int): Código de retorno de connect_ex

    Returns:
        str: Estado inferido da porta
    """

    if codigo == 0:
        return "ABERTA"

    if codigo == errno.ECONNREFUSED:
        return "FECHADA"

    if codigo in (errno.ETIMEDOUT, errno.ENETUNREACH, errno.EHOSTUNREACH):
        return "FILTRADA/INACESSIVEL"

    if codigo == errno.EACCES:
        return "BLOQUEADA (permissao)"

    return "INDETERMINADA"


def testar_porta(host: str, porta: int) -> Dict:
    """
    Executa connect_ex contra o alvo e coleta código de retorno, estado inferido e tempo decorrido

    Args:
        host (str): Endereço IP ou hostname do alvo
        porta (int): Porta TCP a testar

    Returns:
        Dict: Dicionário com os campos 'codigo', 'estado', 'interpretacao' e 'tempo_ms'
    """

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_CONEXAO)

        t_inicio = time.perf_counter()
        codigo = sock.connect_ex((host, porta))
        t_fim = time.perf_counter()

        tempo_ms = (t_fim - t_inicio) * 1000

        return {
            "codigo": codigo,
            "estado": inferir_estado(codigo),
            "interpretacao": interpretar_codigo(codigo),
            "tempo_ms": round(tempo_ms, 2),
        }

    except socket.timeout:
        return {
            "codigo": errno.ETIMEDOUT,
            "estado": inferir_estado(errno.ETIMEDOUT),
            "interpretacao": interpretar_codigo(errno.ETIMEDOUT),
            "tempo_ms": round(TIMEOUT_CONEXAO * 1000, 2),
        }

    except OSError as e:
        return {
            "codigo": e.errno,
            "estado": inferir_estado(e.errno),
            "interpretacao": interpretar_codigo(e.errno),
            "tempo_ms": 0.0,
        }

    finally:
        if sock:
            sock.close()


def executar_diagnostico() -> List[Dict]:
    """
    Percorre todos os alvos definidos, executa o teste de porta e consolida os resultados

    Returns:
        List[Dict]: Lista de dicionários com os dados completos de cada teste
    """

    resultados = []

    for alvo in ALVOS:
        registrar(f"Testando {alvo['host']}:{alvo['porta']}  ({alvo['rotulo']})")
        resultado = testar_porta(alvo["host"], alvo["porta"])
        resultado["rotulo"] = alvo["rotulo"]
        resultado["categoria"] = alvo["categoria"]
        resultado["porta"] = alvo["porta"]

        registrar(f"  Código: {resultado['codigo']}  Estado: {resultado['estado']}  Tempo: {resultado['tempo_ms']} ms")
        registrar(f"  Interpretação: {resultado['interpretacao']}")

        resultados.append(resultado)

    return resultados


def exibir_tabela(resultados: List[Dict]) -> None:
    """
    Exibe os resultados do diagnóstico em formato tabular

    Args:
        resultados (List[Dict]): Lista retornada por executar_diagnostico
    """

    col_porta = 6
    col_categ = 10
    col_rotulo = 40
    col_codigo = 7
    col_estado = 22
    col_tempo = 12

    sep = (f"+{'-' * (col_porta + 2)}+{'-' * (col_categ + 2)}+{'-' * (col_rotulo + 2)}+{'-' * (col_codigo + 2)}+{'-' * (col_estado + 2)}+{'-' * (col_tempo + 2)}+")

    cab = (f"| {'Porta':^{col_porta}} | {'Categoria':^{col_categ}} | {'Descrição':^{col_rotulo}} | {'errno':^{col_codigo}} | {'Estado inferido':^{col_estado}} | {'Tempo (ms)':^{col_tempo}} |")

    print(f"\n{'=' * 100}")
    print("DIAGNÓSTICO DE CONECTIVIDADE TCP COM connect_ex()")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        print(f"| {str(r['porta']):^{col_porta}} | {r['categoria']:<{col_categ}} | {r['rotulo']:<{col_rotulo}} | {str(r['codigo']):^{col_codigo}} | {r['estado']:<{col_estado}} | {str(r['tempo_ms']):^{col_tempo}} |")

    print(sep)

    print(f"\n  Alvo testado: {HOST_ALVO}")
    print(f"  Timeout: {TIMEOUT_CONEXAO} s por porta")
    print(f"  Total de testes: {len(resultados)}")


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


resultados = executar_diagnostico()
exibir_tabela(resultados)
exibir_log()
