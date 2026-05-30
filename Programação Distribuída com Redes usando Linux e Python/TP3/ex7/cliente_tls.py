import ssl
import socket
import datetime
import base64
from typing import Dict, List, Tuple


HOSTS_ALVO: List[Tuple[str, int]] = [
    ("www.google.com", 443),
    ("www.github.com", 443),
    ("www.cloudflare.com", 443),
]

TIMEOUT_CONEXAO = 10.0

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


def extrair_campo_dn(dn: Tuple, campo: str) -> str:
    """
    Extrai o valor de um campo específico de um Distinguished Name retornado pelo ssl

    Args:
        dn (Tuple): Estrutura de DN retornada por getpeercert, como subject ou issuer
        campo (str): Nome do campo a extrair, por exemplo commonName ou organizationName

    Returns:
        str: Valor do campo encontrado, ou string vazia se ausente
    """

    for par in dn:
        for chave, valor in par:
            if chave == campo:
                return valor

    return ""


def formatar_data_certificado(data_str: str) -> str:
    """
    Converte a string de data retornada pelo ssl para o formato brasileiro legível

    Args:
        data_str (str): Data no formato retornado por getpeercert, como 'Jan  1 00:00:00 2025 GMT'

    Returns:
        str: Data formatada como 'DD/MM/AAAA HH:MM:SS UTC' ou a string original em caso de falha
    """

    try:
        dt = datetime.datetime.strptime(data_str, "%b %d %H:%M:%S %Y %Z")
        return dt.strftime("%d/%m/%Y %H:%M:%S UTC")

    except ValueError:
        return data_str


def calcular_dias_restantes(data_expiracao: str) -> int:
    """
    Calcula quantos dias restam até a expiração do certificado

    Args:
        data_expiracao (str): Data de expiração no formato retornado por getpeercert

    Returns:
        int: Dias restantes até a expiração, negativo se já expirado
    """

    try:
        dt_exp = datetime.datetime.strptime(data_expiracao, "%b %d %H:%M:%S %Y %Z")
        delta = dt_exp - datetime.datetime.utcnow()
        return delta.days

    except ValueError:
        return 0


def obter_pem(cert_der: bytes) -> str:
    """
    Converte o certificado em formato DER para PEM

    Args:
        cert_der (bytes): Certificado em formato DER retornado por getpeercert(binary_form=True)

    Returns:
        str: Certificado formatado em PEM com cabeçalho e rodapé padrão
    """

    b64 = base64.b64encode(cert_der).decode("ascii")
    linhas = [b64[i:i + 64] for i in range(0, len(b64), 64)]

    return "-----BEGIN CERTIFICATE-----\n" + "\n".join(linhas) + "\n-----END CERTIFICATE-----"


def inspecionar_host(host: str, porta: int) -> Dict:
    """
    Estabelece conexão TLS com o host indicado e coleta todas as informações do handshake e certificado

    Args:
        host (str): Nome do host HTTPS a conectar
        porta (int): Porta TCP a usar, normalmente 443

    Returns:
        Dict: Dicionário com os campos coletados ou indicação de erro
    """

    contexto = ssl.create_default_context()

    try:
        with socket.create_connection((host, porta), timeout=TIMEOUT_CONEXAO) as sock_raw:
            with contexto.wrap_socket(sock_raw, server_hostname=host) as sock_tls:

                cert = sock_tls.getpeercert()
                cert_der = sock_tls.getpeercert(binary_form=True)
                cipher = sock_tls.cipher()
                versao = sock_tls.version()

                subject_cn = extrair_campo_dn(cert.get("subject", ()), "commonName")
                subject_org = extrair_campo_dn(cert.get("subject", ()), "organizationName")
                issuer_cn = extrair_campo_dn(cert.get("issuer", ()), "commonName")
                issuer_org = extrair_campo_dn(cert.get("issuer", ()), "organizationName")

                not_before = cert.get("notBefore", "")
                not_after = cert.get("notAfter",  "")
                dias_restant = calcular_dias_restantes(not_after)

                sans = [v for tipo, v in cert.get("subjectAltName", []) if tipo == "DNS"]

                return {
                    "host": host,
                    "porta": porta,
                    "erro": None,
                    "subject_cn": subject_cn,
                    "subject_org": subject_org,
                    "issuer_cn": issuer_cn,
                    "issuer_org": issuer_org,
                    "not_before": formatar_data_certificado(not_before),
                    "not_after": formatar_data_certificado(not_after),
                    "dias_restantes": dias_restant,
                    "versao_tls": versao,
                    "cipher_nome": cipher[0] if cipher else "",
                    "cipher_protocolo": cipher[1] if cipher else "",
                    "cipher_bits": cipher[2] if cipher else 0,
                    "sans": sans[:6],
                    "pem": obter_pem(cert_der),
                    "cert_raw": cert,
                }

    except ssl.SSLCertVerificationError as e:
        return {"host": host, "porta": porta, "erro": f"Falha na verificação do certificado: {e}"}

    except ssl.SSLError as e:
        return {"host": host, "porta": porta, "erro": f"Erro TLS: {e}"}

    except (socket.timeout, TimeoutError):
        return {"host": host, "porta": porta, "erro": "Timeout ao conectar"}

    except OSError as e:
        return {"host": host, "porta": porta, "erro": f"Erro de socket: {e}"}


def exibir_inspecao(resultado: Dict) -> None:
    """
    Imprime no terminal as informações coletadas de um host de forma estruturada

    Args:
        resultado (Dict): Dicionário retornado por inspecionar_host
    """

    print(f"\n{'=' * 100}")
    print(f"HOST: {resultado['host']}:{resultado['porta']}")
    print(f"{'=' * 100}\n")

    if resultado.get("erro"):
        print(f"  ERRO: {resultado['erro']}\n")
        return

    dias = resultado["dias_restantes"]
    alerta_expiracao = " (ATENÇÃO: expira em breve)" if 0 < dias < 30 else (" (EXPIRADO)" if dias <= 0 else "")

    print("  CERTIFICADO")
    print(f"    Subject CN: {resultado['subject_cn']}")
    print(f"    Subject Org: {resultado['subject_org']}")

    if resultado["sans"]:
        print(f"    SANs: {', '.join(resultado['sans'])}")

    print()
    print("  EMISSOR (ISSUER)")
    print(f"    Issuer CN: {resultado['issuer_cn']}")
    print(f"    Issuer Org: {resultado['issuer_org']}")

    print()
    print("  VALIDADE")
    print(f"    Não antes de: {resultado['not_before']}")
    print(f"    Não após: {resultado['not_after']}{alerta_expiracao}")
    print(f"    Dias restant: {dias}")

    print()
    print("  SESSÃO TLS")
    print(f"    Versão TLS: {resultado['versao_tls']}")
    print(f"    Cipher: {resultado['cipher_nome']}")
    print(f"    Protocolo: {resultado['cipher_protocolo']}")
    print(f"    Bits: {resultado['cipher_bits']}")

    print()
    print("  CERTIFICADO EM FORMATO PEM")

    for linha in resultado["pem"].splitlines():
        print(f"    {linha}")

    print()


def exibir_tabela_resumo(resultados: List[Dict]) -> None:
    """
    Exibe tabela comparativa com os dados principais de todos os hosts inspecionados

    Args:
        resultados (List[Dict]): Lista de dicionários retornados por inspecionar_host
    """

    col_host = 20
    col_versao = 8
    col_cipher = 28
    col_bits = 6
    col_dias = 8
    col_issuer = 26

    sep = (f"+{'-' * (col_host + 2)}+{'-' * (col_versao + 2)}+{'-' * (col_cipher + 2)}+{'-' * (col_bits + 2)}+{'-' * (col_dias + 2)}+{'-' * (col_issuer + 2)}+")
    cab = (f"| {'Host':^{col_host}} | {'TLS':^{col_versao}} | {'Cipher':^{col_cipher}} | {'Bits':^{col_bits}} | {'Dias':^{col_dias}} | {'Issuer CN':^{col_issuer}} |")

    print(f"\n{'=' * 100}")
    print("TABELA RESUMO DE INSPEÇÃO TLS")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        if r.get("erro"):
            print(f"| {r['host']:<{col_host}} | {'ERRO':^{col_versao}} | {r['erro'][:col_cipher]:<{col_cipher}} | {'-':^{col_bits}} | {'-':^{col_dias}} | {'-':^{col_issuer}} |")
        
        else:
            issuer = r["issuer_cn"][:col_issuer]
            print(f"| {r['host']:<{col_host}} | {r['versao_tls']:^{col_versao}} | {r['cipher_nome']:<{col_cipher}} | {str(r['cipher_bits']):^{col_bits}} | {str(r['dias_restantes']):^{col_dias}} | {issuer:<{col_issuer}} |")

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


def executar_inspecao() -> None:
    """
    Percorre todos os hosts definidos, executa a inspeção TLS e exibe os resultados detalhados e o resumo comparativo
    """

    resultados = []

    for host, porta in HOSTS_ALVO:
        registrar(f"Inspecionando {host}:{porta}")
        resultado = inspecionar_host(host, porta)
        resultados.append(resultado)

        if resultado.get("erro"):
            registrar(f"  Erro: {resultado['erro']}")

        else:
            registrar(f"  TLS: {resultado['versao_tls']}  Cipher: {resultado['cipher_nome']}  Dias restantes: {resultado['dias_restantes']}")

        exibir_inspecao(resultado)

    exibir_tabela_resumo(resultados)
    exibir_log()


executar_inspecao()
