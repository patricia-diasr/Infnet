import subprocess
import datetime
from typing import List, Tuple, Dict


HOST_SERVIDOR = "192.168.56.101"
PORTA = 23
LOG: list = []


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log da análise

    Args:
        evento (str): Descrição do evento
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"
    LOG.append(entrada)
    print(entrada)


def executar_curl(args: List[str]) -> Tuple[str, str, int]:
    """
    Executa um comando curl com os argumentos fornecidos e captura a saída completa

    Args:
        args (List[str]): Lista de argumentos a passar para o curl

    Returns:
        Tuple[str, str, int]: (stdout, stderr, código de retorno)
    """

    resultado = subprocess.run(["curl"] + args, capture_output=True, text=True, timeout=15)
    return resultado.stdout, resultado.stderr, resultado.returncode


def extrair_eventos_iac(texto: str) -> List[str]:
    """
    Extrai do texto verbose do curl apenas as linhas que descrevem eventos de protocolo Telnet

    Args:
        texto (str): Saída verbose completa do curl

    Returns:
        List[str]: Linhas que contêm eventos IAC ou de conexão relevantes
    """

    prefixos_relevantes = ("Trying", "Connected", "RCVD", "SENT", "Time-out", "Closing")
    eventos = []

    for linha in texto.splitlines():
        linha_limpa = linha.strip().lstrip("* ").lstrip("== Info: ").strip()

        if any(linha_limpa.startswith(p) for p in prefixos_relevantes):
            eventos.append(linha_limpa)

    return eventos


def traduzir_codigo(codigo: int) -> str:
    """
    Retorna uma descrição legível para os códigos de retorno mais comuns do curl

    Args:
        codigo (int): Código de retorno do processo curl

    Returns:
        str: Descrição do código
    """

    tabela = {
        0: "Sucesso",
        7: "Falha ao conectar",
        28: "Timeout (esperado em Telnet sem dados)",
        35: "Erro SSL/TLS",
        56: "Falha ao receber dados",
    }

    return tabela.get(codigo, f"Código desconhecido ({codigo})")


def exibir_bloco_detalhado(numero: int, descricao: str, stdout: str, stderr: str, codigo: int) -> None:
    """
    Exibe o resultado completo e anotado de um teste curl individual

    Args:
        numero (int): Número sequencial do teste
        descricao (str): Descrição do objetivo do teste
        stdout (str): Saída padrão capturada do curl
        stderr (str): Saída de erro capturada do curl
        codigo (int): Código de retorno do processo
    """

    texto_completo = stdout + stderr
    eventos = extrair_eventos_iac(texto_completo)

    print(f"\n--- Teste {numero}: {descricao} ---\n")
    print(f"  Código de retorno : {codigo} - {traduzir_codigo(codigo)}")
    print(f"  Eventos de protocolo observados:")

    if eventos:
        for evento in eventos:
            print(f"    {evento}")

    else:
        print("    (nenhum evento de protocolo capturado)")

    print()


def exibir_tabela_resumo(resultados: List[Dict]) -> None:
    """
    Exibe uma tabela consolidada com os dados extraídos de todos os testes curl

    Args:
        resultados (List[Dict]): Lista de dicionários com os dados de cada teste
    """

    col_n = 4
    col_desc = 42
    col_cod = 6
    col_trad = 38
    col_iac = 5

    sep = f"+{'-' * (col_n + 2)}+{'-' * (col_desc + 2)}+{'-' * (col_cod + 2)}+{'-' * (col_trad + 2)}+{'-' * (col_iac + 2)}+"
    cab = (f"| {'#':^{col_n}} | {'Teste':^{col_desc}} | {'Cód.':^{col_cod}} | {'Interpretação':^{col_trad}} | {'IAC':^{col_iac}} |")

    print(f"\n{'='*100}")
    print("  TABELA RESUMO - ANÁLISE CURL")
    print(f"{'='*100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        iac_obs = "Sim" if r["iac_observado"] else "Não"
        print(f"| {str(r['numero']):^{col_n}} | {r['descricao']:<{col_desc}} | {str(r['codigo']):^{col_cod}} | {traduzir_codigo(r['codigo']):<{col_trad}} | {iac_obs:^{col_iac}} |")

    print(sep)


def executar_bateria_curl() -> None:
    """
    Executa os testes curl contra o servidor Telnet, exibe os blocos detalhados e a tabela de resumo com os dados extraídos de cada execução
    """

    url = f"telnet://{HOST_SERVIDOR}:{PORTA}"

    testes: List[Tuple[str, List[str]]] = [
        (
            "Handshake e negociação IAC (verbose)",
            ["--verbose", "--max-time", "4", url]
        ),
        (
            "Rastreamento de bytes brutos (trace-ascii)",
            ["--trace-ascii", "-", "--max-time", "4", url]
        ),
        (
            "Envio de comando 'hostname' via pipe",
            ["--verbose", "--max-time", "4", "--data", "hostname\n", url]
        ),
        (
            "Verificação de porta sem payload",
            ["--verbose", "--max-time", "3", "--connect-timeout", "3", url]
        ),
    ]

    print(f"\n{'='*100}")
    print("  BLOCOS DETALHADOS - ANÁLISE CURL")
    print(f"{'='*100}")

    resultados = []

    for i, (descricao, args) in enumerate(testes, 1):
        registrar(f"Executando teste {i}: {descricao}")

        try:
            stdout, stderr, codigo = executar_curl(args)
            texto_completo = stdout + stderr
            eventos = extrair_eventos_iac(texto_completo)
            iac_observado = any("RCVD" in e or "SENT" in e for e in eventos)
            exibir_bloco_detalhado(i, descricao, stdout, stderr, codigo)

            resultados.append({
                "numero": i,
                "descricao": descricao,
                "codigo": codigo,
                "iac_observado": iac_observado,
            })

        except subprocess.TimeoutExpired:
            registrar(f"Processo curl excedeu o timeout do Python no teste {i}")

            resultados.append({
                "numero": i,
                "descricao": descricao,
                "codigo": -1,
                "iac_observado": False,
            })

    exibir_tabela_resumo(resultados)

    print(f"\n\n{'='*100}")
    print("  LOG DA ANÁLISE")
    print(f"{'='*100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


executar_bateria_curl()
