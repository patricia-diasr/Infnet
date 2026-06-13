import re
import sys
from typing import List, Dict, Optional, Tuple


ARQUIVO_TRACE = "trace_http.txt"


def ler_linhas_trace(caminho: str) -> List[str]:
    """
    Lê o arquivo de trace e retorna todas as linhas como lista

    Args:
        caminho (str): Caminho para o arquivo de trace gerado pelo curl

    Returns:
        List[str]: Lista de linhas do arquivo
    """

    with open(caminho, "r", encoding="utf-8", errors="replace") as arquivo:
        return arquivo.readlines()


def extrair_ip_remoto(linhas: List[str]) -> Optional[str]:
    """
    Extrai o IP remoto da linha de conexão registrada pelo curl no trace

    Args:
        linhas (List[str]): Linhas do arquivo de trace

    Returns:
        Optional[str]: IP remoto encontrado ou None se não identificado
    """

    for linha in linhas:
        linha_limpa = linha.strip()

        if "Connected to" in linha_limpa:
            partes = linha_limpa.split("(")

            if len(partes) >= 2:
                ip = partes[1].split(")")[0].strip()
                return ip

    return None


def extrair_bloco_requisicao(linhas: List[str]) -> List[str]:
    """
    Extrai as linhas de texto do bloco de dados enviados ao servidor, identificado pelo marcador Send header e pelas linhas no formato offset conteúdo

    Args:
        linhas (List[str]): Linhas do arquivo de trace

    Returns:
        List[str]: Linhas de texto puro da requisição HTTP
    """

    return _extrair_bloco(linhas, "=> Send header")


def extrair_bloco_resposta(linhas: List[str]) -> List[str]:
    """
    Extrai as linhas de texto do bloco de dados recebidos do servidor, identificado pelo marcador Recv header e pelas linhas no formato offset conteúdo

    Args:
        linhas (List[str]): Linhas do arquivo de trace

    Returns:
        List[str]: Linhas de texto puro da resposta HTTP
    """

    return _extrair_bloco(linhas, "<= Recv header")


def _extrair_bloco(linhas: List[str], marcador: str) -> List[str]:
    """
    Percorre as linhas do trace e coleta o conteúdo textual associado a um marcador de envio ou recebimento

    Args:
        linhas (List[str]): Linhas do arquivo de trace
        marcador (str): Texto do marcador que indica o início do bloco desejado

    Returns:
        List[str]: Linhas de texto puro associadas ao marcador
    """

    padrao_offset = re.compile(r"^[0-9a-fA-F]{4,}:\s?(.*)$")
    capturando = False
    bloco: List[str] = []

    for linha in linhas:
        linha_sem_quebra = linha.rstrip("\n")

        if marcador in linha_sem_quebra:
            capturando = True
            continue

        if "=> Send header" in linha_sem_quebra or "<= Recv header" in linha_sem_quebra:
            capturando = False
            continue

        if linha_sem_quebra.startswith("==") or linha_sem_quebra.startswith("*"):
            capturando = False
            continue

        if capturando:
            correspondencia = padrao_offset.match(linha_sem_quebra)

            if correspondencia:
                conteudo = correspondencia.group(1).rstrip("\r")

                if conteudo:
                    bloco.append(conteudo)

    return bloco


def parsear_requisicao(linhas_req: List[str]) -> Tuple[str, str]:
    """
    Extrai o método HTTP e o host da requisição capturada no trace

    Args:
        linhas_req (List[str]): Linhas de texto da requisição HTTP

    Returns:
        Tuple[str, str]: (método HTTP, valor do header Host)
    """

    metodo = "Não identificado"
    host = "Não identificado"

    for linha in linhas_req:
        if linha.startswith("GET") or linha.startswith("POST") or linha.startswith("HEAD"):
            metodo = linha.split(" ")[0]

        if linha.lower().startswith("host:"):
            host = linha.split(":", 1)[1].strip()

    return metodo, host


def parsear_resposta(linhas_resp: List[str]) -> Tuple[str, Dict[str, str]]:
    """
    Extrai o status code e os headers principais da resposta HTTP capturada no trace

    Args:
        linhas_resp (List[str]): Linhas de texto da resposta HTTP

    Returns:
        Tuple[str, Dict[str, str]]: (linha de status, dicionário de headers)
    """

    status = "Não identificado"
    headers: Dict[str, str] = {}
    headers_relevantes = {"content-type", "content-length", "server", "location", "date", "cache-control"}

    for linha in linhas_resp:
        if linha.startswith("HTTP") and status == "Não identificado":
            status = linha.strip()
            continue

        if ":" in linha:
            chave, _, valor = linha.partition(":")
            chave_norm = chave.strip().lower()

            if chave_norm in headers_relevantes:
                headers[chave.strip()] = valor.strip()

    return status, headers


def exibir_resultado(metodo: str, host: str, status: str, headers: Dict[str, str], ip: Optional[str]) -> None:
    """
    Exibe no terminal os dados extraídos do trace HTTP de forma organizada

    Args:
        metodo (str): Método HTTP identificado na requisição
        host (str): Valor do header Host da requisição
        status (str): Linha de status da resposta HTTP
        headers (Dict[str, str]): Headers principais da resposta
        ip (Optional[str]): IP remoto utilizado na conexão
    """

    print(f"\n{'=' * 60}")
    print("ANÁLISE DO TRACE HTTP")
    print(f"{'=' * 60}\n")
    print(f"  Método HTTP: {metodo}")
    print(f"  Host: {host}")
    print(f"  Status: {status}")
    print(f"  IP remoto: {ip if ip else 'Não identificado'}")
    print(f"\n  Headers da resposta:")

    if headers:
        for chave, valor in headers.items():
            print(f"    {chave}: {valor}")

    else:
        print("    (nenhum header relevante identificado)")

    print()


def analisar_trace(caminho: str) -> None:
    """
    Coordena a leitura e análise completa do arquivo de trace gerado pelo curl

    Args:
        caminho (str): Caminho para o arquivo de trace
    """

    linhas = ler_linhas_trace(caminho)
    ip = extrair_ip_remoto(linhas)
    linhas_req = extrair_bloco_requisicao(linhas)
    linhas_resp = extrair_bloco_resposta(linhas)
    metodo, host = parsear_requisicao(linhas_req)
    status, headers = parsear_resposta(linhas_resp)
    exibir_resultado(metodo, host, status, headers, ip)


analisar_trace(ARQUIVO_TRACE)
