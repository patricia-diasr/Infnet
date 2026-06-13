from typing import List, Dict
from scapy.all import sniff, TCP, Raw, Packet


INTERFACE = "enp0s3"
PORTA_SERVIDOR = 8080
TEMPO_CAPTURA = 600
ARQUIVO_LOG = "acessos.log"
LIMITE_OCORRENCIAS = 3


def processar_pacote(pacote: Packet) -> None:
    """
    Analisa um pacote capturado e exibe a linha de requisição HTTP se presente

    Args:
        pacote (Packet): Pacote TCP capturado pelo Scapy
    """

    if not pacote.haslayer(TCP) or not pacote.haslayer(Raw):
        return

    payload = bytes(pacote[Raw].load)
    texto = payload.decode("utf-8", errors="ignore")

    if texto.startswith("GET") or texto.startswith("POST") or texto.startswith("HEAD"):
        primeira_linha = texto.split("\r\n")[0]
        print(f"  Requisição capturada de {pacote.src}: {primeira_linha}")


def executar_captura(interface: str, porta: int, tempo: int) -> None:
    """
    Captura pacotes HTTP na porta do servidor durante o tempo configurado

    Args:
        interface (str): Nome da interface de rede a monitorar
        porta (int): Porta TCP do servidor HTTP
        tempo (int): Duração da captura em segundos
    """

    filtro = f"tcp port {porta}"

    print(f"\n{'=' * 60}")
    print("CAPTURA DE TRÁFEGO HTTP")
    print(f"{'=' * 60}\n")
    print(f"  Interface: {interface}")
    print(f"  Filtro BPF: {filtro}")
    print(f"  Duração: {tempo} segundos\n")

    sniff(iface=interface, filter=filtro, prn=processar_pacote, store=False, timeout=tempo)


def ler_registros_log(caminho: str) -> List[Dict[str, str]]:
    """
    Lê o arquivo de log de acessos e retorna os registros como lista de dicionários

    Args:
        caminho (str): Caminho do arquivo de log de acessos

    Returns:
        List[Dict[str, str]]: Lista de registros com timestamp, ip, metodo, endpoint e status
    """

    registros: List[Dict[str, str]] = []

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                campos = [c.strip() for c in linha.strip().split("|")]

                if len(campos) == 5:
                    registros.append({
                        "timestamp": campos[0],
                        "ip": campos[1],
                        "metodo": campos[2],
                        "endpoint": campos[3],
                        "status": campos[4],
                    })

    except FileNotFoundError:
        print(f"  Arquivo de log {caminho} não encontrado")

    return registros


def detectar_acessos_invalidos(registros: List[Dict[str, str]], limite: int) -> Dict[str, int]:
    """
    Identifica IPs com três ou mais acessos a paths inválidos registrados como status 404

    Args:
        registros (List[Dict[str, str]]): Registros de acesso extraídos do log
        limite (int): Quantidade mínima de ocorrências para caracterizar o padrão anômalo

    Returns:
        Dict[str, int]: Dicionário com IPs identificados e a quantidade de acessos inválidos
    """

    contagem: Dict[str, int] = {}

    for registro in registros:
        if registro["status"] == "404":
            ip = registro["ip"]
            contagem[ip] = contagem.get(ip, 0) + 1

    return {ip: total for ip, total in contagem.items() if total >= limite}


def exibir_anomalias(anomalias: Dict[str, int], limite: int) -> None:
    """
    Exibe no terminal os IPs que apresentaram o padrão anômalo identificado

    Args:
        anomalias (Dict[str, int]): IPs e respectivas contagens de acessos inválidos
        limite (int): Quantidade mínima de ocorrências utilizada como critério
    """

    print(f"\n{'=' * 60}")
    print("ANÁLISE DO LOG DE ACESSOS")
    print(f"{'=' * 60}\n")
    print(f"  Critério: acesso a path inválido com {limite} ou mais ocorrências do mesmo IP\n")

    if anomalias:
        for ip, total in anomalias.items():
            print(f"  IP {ip} apresentou {total} acessos a paths inválidos")

    else:
        print("  Nenhum padrão anômalo identificado")

    print()


def executar_analise(interface: str, porta: int, tempo: int, caminho_log: str, limite: int) -> None:
    """
    Coordena a captura de tráfego HTTP e a análise do log de acessos em busca de anomalias

    Args:
        interface (str): Nome da interface de rede a monitorar
        porta (int): Porta TCP do servidor HTTP
        tempo (int): Duração da captura em segundos
        caminho_log (str): Caminho do arquivo de log de acessos
        limite (int): Quantidade mínima de ocorrências para caracterizar o padrão anômalo
    """

    executar_captura(interface, porta, tempo)
    registros = ler_registros_log(caminho_log)
    anomalias = detectar_acessos_invalidos(registros, limite)
    exibir_anomalias(anomalias, limite)


executar_analise(INTERFACE, PORTA_SERVIDOR, TEMPO_CAPTURA, ARQUIVO_LOG, LIMITE_OCORRENCIAS)
