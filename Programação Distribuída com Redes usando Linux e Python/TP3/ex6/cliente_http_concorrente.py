import socket
import subprocess
import threading
import datetime
import time
from typing import List, Dict


HOST_SERVIDOR = "127.0.0.1"
PORTA = 8080

TOTAL_REQUISICOES = 10
CAMINHO = "/health"
TAMANHO_BUFFER = 4096

LOG: list = []
lock_resultados = threading.Lock()
lock_log = threading.Lock()


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log compartilhado entre threads

    Args:
        evento (str): Descrição do evento ocorrido
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"

    with lock_log:
        LOG.append(entrada)
        print(entrada)


def montar_requisicao(caminho: str) -> bytes:
    """
    Monta uma requisição GET HTTP/1.1 mínima válida

    Args:
        caminho (str): Caminho do recurso a requisitar

    Returns:
        bytes: Requisição HTTP serializada
    """

    requisicao = (
        f"GET {caminho} HTTP/1.1\r\n"
        f"Host: {HOST_SERVIDOR}:{PORTA}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return requisicao.encode("utf-8")


def extrair_status(dados: bytes) -> str:
    """
    Extrai a status line da resposta HTTP recebida

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        str: Status line extraída ou indicação de ausência
    """

    try:
        texto = dados.decode("utf-8", errors="replace")
        return texto.splitlines()[0] if texto.splitlines() else "(sem status)"

    except Exception:
        return "(erro ao extrair status)"


def extrair_headers(dados: bytes) -> Dict[str, str]:
    """
    Extrai o dicionário de headers da resposta HTTP recebida

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        Dict[str, str]: Dicionário com chaves e valores dos cabeçalhos HTTP
    """

    headers = {}

    try:
        texto = dados.decode("utf-8", errors="replace")
        separador = "\r\n\r\n"
        pos = texto.find(separador)

        if pos == -1:
            return headers

        cabecalho = texto[:pos]

        for linha in cabecalho.splitlines()[1:]:
            if ":" in linha:
                chave, _, valor = linha.partition(":")
                headers[chave.strip()] = valor.strip()

    except Exception:
        pass

    return headers


def extrair_corpo(dados: bytes) -> str:
    """
    Extrai o corpo da resposta HTTP a partir do separador de cabeçalho

    Args:
        dados (bytes): Bytes brutos da resposta HTTP

    Returns:
        str: Corpo da resposta como texto
    """

    try:
        separador = b"\r\n\r\n"
        pos = dados.find(separador)

        if pos == -1:
            return ""

        return dados[pos + len(separador):].decode("utf-8", errors="replace")

    except Exception:
        return ""


def executar_requisicao(id_req: int, resultados: List[Dict]) -> None:
    """
    Executa uma requisição GET via socket puro, coleta status, headers e payload e registra o resultado

    Args:
        id_req (int): Identificador sequencial da requisição
        resultados (List[Dict]): Lista compartilhada onde o resultado será appendado
    """

    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST_SERVIDOR, PORTA))

        ip_local, porta_local = sock.getsockname()
        t_inicio = time.perf_counter()

        sock.sendall(montar_requisicao(CAMINHO))

        dados = b""

        while True:
            fragmento = sock.recv(TAMANHO_BUFFER)

            if not fragmento:
                break

            dados += fragmento

        t_fim = time.perf_counter()
        latencia = round((t_fim - t_inicio) * 1000, 2)
        status = extrair_status(dados)
        headers = extrair_headers(dados)
        corpo = extrair_corpo(dados)
        sucesso = "200" in status

        registrar(f"  Req {id_req:02d}  porta local {porta_local}  {status}  {latencia} ms")

        with lock_resultados:
            resultados.append({
                "id": id_req,
                "porta_local": porta_local,
                "status": status,
                "headers": headers,
                "corpo": corpo,
                "latencia_ms": latencia,
                "sucesso": sucesso,
            })

    except ConnectionRefusedError:
        registrar(f"  Req {id_req:02d}  erro: conexão recusada")

        with lock_resultados:
            resultados.append({
                "id": id_req, "porta_local": None, "status": "ERRO: conexão recusada",
                "headers": {}, "corpo": "", "latencia_ms": None, "sucesso": False,
            })

    except OSError as e:
        registrar(f"  Req {id_req:02d}  erro: {e}")

        with lock_resultados:
            resultados.append({
                "id": id_req, "porta_local": None, "status": f"ERRO: {e}",
                "headers": {}, "corpo": "", "latencia_ms": None, "sucesso": False,
            })

    finally:
        if sock:
            sock.close()


def lancar_requisicoes_simultaneas() -> List[Dict]:
    """
    Dispara as requisições em threads simultâneas e aguarda a conclusão de todas

    Returns:
        List[Dict]: Lista com os resultados de todas as requisições
    """

    resultados: List[Dict] = []
    threads = []

    registrar(f"Disparando {TOTAL_REQUISICOES} requisições simultâneas para GET {CAMINHO}")

    for i in range(1, TOTAL_REQUISICOES + 1):
        t = threading.Thread(
            target=executar_requisicao,
            args=(i, resultados),
            daemon=True
        )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return resultados


def exibir_tabela(resultados: List[Dict]) -> None:
    """
    Exibe a tabela consolidada com os resultados de todas as requisições

    Args:
        resultados (List[Dict]): Lista de resultados retornada por lancar_requisicoes_simultaneas
    """

    resultados_ord = sorted(resultados, key=lambda r: r["id"])

    col_id = 4
    col_porta = 15
    col_status = 28
    col_lat = 14
    col_suc = 8

    sep = (f"+{'-' * (col_id + 2)}+{'-' * (col_porta + 2)}+{'-' * (col_status + 2)}+{'-' * (col_lat + 2)}+{'-' * (col_suc + 2)}+")
    cab = (f"| {'#':^{col_id}} | {'Porta local':^{col_porta}} | {'Status':^{col_status}} | {'Latência (ms)':^{col_lat}} | {'Sucesso':^{col_suc}} |")

    print(f"\n{'=' * 100}")
    print("RESULTADOS DAS REQUISIÇÕES SIMULTÂNEAS")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados_ord:
        porta = str(r["porta_local"]) if r["porta_local"] else "-"
        lat = f"{r['latencia_ms']:.2f}" if r["latencia_ms"] is not None else "-"
        sucesso = "Sim" if r["sucesso"] else "Não"

        print(f"| {str(r['id']):^{col_id}} | {porta:^{col_porta}} | {r['status']:<{col_status}} | {lat:^{col_lat}} | {sucesso:^{col_suc}} |")

    print(sep)

    bem_sucedidas = sum(1 for r in resultados if r["sucesso"])
    falhas = len(resultados) - bem_sucedidas
    latencias = [r["latencia_ms"] for r in resultados if r["latencia_ms"] is not None]
    media_lat = sum(latencias) / len(latencias) if latencias else 0

    print(f"\n  Requisições enviadas: {len(resultados)}")
    print(f"  Respostas bem-sucedidas: {bem_sucedidas}")
    print(f"  Falhas: {falhas}")
    print(f"  Latência média: {media_lat:.2f} ms")

    if resultados_ord:
        primeiro = resultados_ord[0]

        if primeiro["headers"]:
            print(f"\n{'=' * 100}")
            print("HEADERS DE UMA RESPOSTA (requisição 1)")
            print(f"{'=' * 100}\n")

            for chave, valor in primeiro["headers"].items():
                print(f"  {chave}: {valor}")

        if primeiro["corpo"]:
            print(f"\n{'=' * 100}")
            print("  PAYLOAD DE UMA RESPOSTA (requisição 1)")
            print(f"{'=' * 100}\n")

            for linha in primeiro["corpo"].splitlines():
                print(f"  {linha}")


def exibir_curl() -> None:
    """
    Executa as 10 requisições simultâneas ao endpoint /health via curl e exibe as saídas capturadas
    """

    url = f"http://{HOST_SERVIDOR}:{PORTA}{CAMINHO}"

    registrar(f"Disparando 10 requisições via curl para {url}")

    processos = []

    for i in range(1, TOTAL_REQUISICOES + 1):
        proc = subprocess.Popen(
            ["curl", "-s", "-o", "/dev/null", "-w", f"curl {i:02d}: %{{http_code}} - %{{time_total}}s\n", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processos.append((i, proc))

    print(f"\n{'=' * 100}")
    print("  SAÍDAS DO CURL (10 REQUISIÇÕES SIMULTÂNEAS)")
    print(f"{'=' * 100}\n")

    for id_req, proc in processos:
        stdout, _ = proc.communicate(timeout=10)

        if stdout.strip():
            print(f"  {stdout.strip()}")


def exibir_log() -> None:
    """
    Exibe o log completo da execução ao final do programa
    """

    print(f"\n{'=' * 100}")
    print("  LOG DA EXECUÇÃO")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


registrar(f"Cliente HTTP iniciado, alvo: {HOST_SERVIDOR}:{PORTA}")
exibir_curl()
resultados = lancar_requisicoes_simultaneas()
exibir_tabela(resultados)
exibir_log()
