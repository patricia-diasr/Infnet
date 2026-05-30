import socket
import datetime
import time
import errno
from typing import List, Dict


HOST_ALVO = "127.0.0.1"
PORTA_INICIAL = 1
PORTA_FINAL = 1024
TIMEOUT = 0.5

TABELA_SERVICOS: Dict[int, str] = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP alternativo",
    8443: "HTTPS alternativo",
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


def identificar_servico(porta: int) -> str:
    """
    Retorna o nome do serviço convencional associado à porta, se conhecido

    Args:
        porta (int): Número da porta TCP

    Returns:
        str: Nome do serviço ou string vazia se não mapeado
    """

    return TABELA_SERVICOS.get(porta, "")


def testar_porta(host: str, porta: int, timeout: float) -> Dict:
    """
    Testa uma porta TCP usando connect_ex e retorna o resultado com código errno e tempo decorrido

    Args:
        host (str): Endereço IP do alvo
        porta (int): Porta TCP a testar
        timeout (float): Tempo máximo de espera pela conexão em segundos

    Returns:
        Dict: Dicionário com os campos 'porta', 'aberta', 'codigo_errno' e 'tempo_ms'
    """

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        t_inicio = time.perf_counter()
        codigo = sock.connect_ex((host, porta))
        t_fim = time.perf_counter()

        tempo_ms = round((t_fim - t_inicio) * 1000, 2)
        aberta = codigo == 0

        return {
            "porta": porta,
            "aberta": aberta,
            "codigo_errno": codigo,
            "tempo_ms": tempo_ms,
        }

    except socket.timeout:
        return {
            "porta": porta,
            "aberta": False,
            "codigo_errno": errno.ETIMEDOUT,
            "tempo_ms": round(timeout * 1000, 2),
        }

    except OSError as e:
        return {
            "porta": porta,
            "aberta": False,
            "codigo_errno": e.errno if e.errno else -1,
            "tempo_ms": 0.0,
        }

    finally:
        if sock:
            sock.close()


def executar_varredura(host: str, porta_ini: int, porta_fim: int, timeout: float) -> List[Dict]:
    """
    Executa a varredura TCP síncrona no intervalo de portas indicado e retorna apenas as abertas

    Args:
        host (str): Endereço IP do alvo
        porta_ini (int): Primeira porta do intervalo (inclusiva)
        porta_fim (int): Última porta do intervalo (inclusiva)
        timeout (float): Timeout individual por porta em segundos

    Returns:
        List[Dict]: Lista de resultados apenas das portas abertas detectadas
    """

    total = porta_fim - porta_ini + 1
    abertas = []
    testadas = 0

    registrar(f"Iniciando varredura em {host}  portas {porta_ini} até {porta_fim}  ({total} portas)  timeout={timeout}s")

    for porta in range(porta_ini, porta_fim + 1):
        resultado = testar_porta(host, porta, timeout)
        testadas += 1

        if resultado["aberta"]:
            servico = identificar_servico(porta)
            registrar(f"  Porta {porta:5d} ABERTA  {servico}  tempo={resultado['tempo_ms']}ms")
            resultado["servico"] = servico
            abertas.append(resultado)

        if testadas % 100 == 0:
            registrar(f"  Progresso: {testadas}/{total} portas testadas  abertas até agora: {len(abertas)}")

    return abertas


def exibir_tabela_portas_abertas(abertas: List[Dict], host: str, tempo_total_s: float) -> None:
    """
    Exibe a tabela com as portas abertas detectadas e o resumo da varredura

    Args:
        abertas (List[Dict]): Lista de resultados das portas abertas
        host (str): Endereço IP varrido
        tempo_total_s (float): Tempo total da varredura em segundos
    """

    col_porta = 8
    col_servico = 22
    col_errno = 8
    col_tempo = 14

    sep = (f"+{'-' * (col_porta + 2)}+{'-' * (col_servico + 2)}+{'-' * (col_errno + 2)}+{'-' * (col_tempo + 2)}+")
    cab = (f"| {'Porta':^{col_porta}} | {'Serviço':^{col_servico}} | {'errno':^{col_errno}} | {'Tempo (ms)':^{col_tempo}} |")

    print(f"\n{'=' * 100}")
    print("PORTAS ABERTAS DETECTADAS")
    print(f"{'=' * 100}\n")

    if not abertas:
        print("  Nenhuma porta aberta detectada no intervalo.\n")
    
    else:
        print(sep)
        print(cab)
        print(sep)

        for r in abertas:
            servico = r.get("servico", "")
            print(f"| {str(r['porta']):^{col_porta}} | {servico:<{col_servico}} | {str(r['codigo_errno']):^{col_errno}} | {str(r['tempo_ms']):^{col_tempo}} |")

        print(sep)

    total_intervalo = PORTA_FINAL - PORTA_INICIAL + 1

    print(f"\n  Host varrido: {host}")
    print(f"  Intervalo: {PORTA_INICIAL} a {PORTA_FINAL}")
    print(f"  Total de portas: {total_intervalo}")
    print(f"  Portas abertas: {len(abertas)}")
    print(f"  Tempo total: {tempo_total_s:.2f} s")
    print(f"  Média por porta: {(tempo_total_s / total_intervalo * 1000):.2f} ms")


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


t_inicio_total = time.perf_counter()
abertas = executar_varredura(HOST_ALVO, PORTA_INICIAL, PORTA_FINAL, TIMEOUT)
t_fim_total = time.perf_counter()
tempo_total = round(t_fim_total - t_inicio_total, 2)

registrar(f"Varredura concluída em {tempo_total}s  {len(abertas)} porta(s) aberta(s) detectada(s)")

exibir_tabela_portas_abertas(abertas, HOST_ALVO, tempo_total)
exibir_log()
