import nmap
from typing import List, Dict


HOST_ALVO = "127.0.0.1"
FAIXA_PORTAS = "1-1024"


def executar_varredura(host: str, portas: str) -> nmap.PortScanner:
    """
    Executa uma varredura de portas TCP no host informado usando nmap

    Args:
        host (str): Endereço IP ou hostname alvo da varredura
        portas (str): Faixa de portas a varrer no formato aceito pelo nmap

    Returns:
        nmap.PortScanner: Objeto scanner contendo os resultados da varredura
    """

    scanner = nmap.PortScanner()
    scanner.scan(hosts=host, ports=portas, arguments="-sT")
    return scanner


def extrair_resultados(scanner: nmap.PortScanner, host: str) -> List[Dict[str, str]]:
    """
    Extrai porta, estado e serviço identificado de cada porta TCP encontrada na varredura

    Args:
        scanner (nmap.PortScanner): Objeto scanner já executado com os resultados
        host (str): Endereço IP ou hostname que foi varrido

    Returns:
        List[Dict[str, str]]: Lista de dicionários contendo porta, estado e serviço
    """

    resultados: List[Dict[str, str]] = []

    if host not in scanner.all_hosts():
        return resultados

    portas_tcp = scanner[host].get("tcp", {})

    for porta in sorted(portas_tcp.keys()):
        info = portas_tcp[porta]
        resultados.append({
            "porta": str(porta),
            "estado": info.get("state", "desconhecido"),
            "servico": info.get("name", "desconhecido"),
        })

    return resultados


def exibir_resultados(host: str, portas: str, resultados: List[Dict[str, str]]) -> None:
    """
    Exibe em formato de tabela as portas, estados e serviços identificados na varredura

    Args:
        host (str): Endereço IP ou hostname que foi varrido
        portas (str): Faixa de portas utilizada na varredura
        resultados (List[Dict[str, str]]): Lista de dicionários com porta, estado e serviço
    """

    print(f"\n{'=' * 60}")
    print("  VARREDURA DE PORTAS COM PYTHON NMAP")
    print(f"{'=' * 60}\n")
    print(f"  Host alvo: {host}")
    print(f"  Faixa: {portas}\n")

    if not resultados:
        print("  Nenhuma porta aberta foi identificada\n")
        return

    col_porta = 8
    col_estado = 12
    col_servico = 20

    sep = f"+{'-' * (col_porta + 2)}+{'-' * (col_estado + 2)}+{'-' * (col_servico + 2)}+"
    cab = f"| {'Porta':^{col_porta}} | {'Estado':^{col_estado}} | {'Serviço':^{col_servico}} |"

    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        print(f"| {r['porta']:^{col_porta}} | {r['estado']:^{col_estado}} | {r['servico']:<{col_servico}} |")

    print(sep)
    print()


def executar_inventario(host: str, portas: str) -> None:
    """
    Coordena a execução da varredura local e a exibição dos resultados encontrados

    Args:
        host (str): Endereço IP ou hostname alvo da varredura
        portas (str): Faixa de portas a varrer no formato aceito pelo nmap
    """

    scanner = executar_varredura(host, portas)
    resultados = extrair_resultados(scanner, host)
    exibir_resultados(host, portas, resultados)


executar_inventario(HOST_ALVO, FAIXA_PORTAS)
