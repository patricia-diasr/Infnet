import dns.resolver
from typing import List, Tuple


DOMINIO = "www.google.com"


def resolver_registros_a(dominio: str) -> List[str]:
    """
    Consulta e retorna todos os registros A (IPv4) encontrados para o domínio

    Args:
        dominio (str): Nome de domínio a consultar

    Returns:
        List[str]: Lista de endereços IPv4 resolvidos
    """

    try:
        resposta = dns.resolver.resolve(dominio, "A")
        return [str(registro) for registro in resposta]

    except dns.resolver.NoAnswer:
        return []

    except dns.resolver.NXDOMAIN:
        return []

    except Exception as erro:
        return [f"Erro: {erro}"]


def resolver_registros_aaaa(dominio: str) -> List[str]:
    """
    Consulta e retorna todos os registros AAAA (IPv6) encontrados para o domínio

    Args:
        dominio (str): Nome de domínio a consultar

    Returns:
        List[str]: Lista de endereços IPv6 resolvidos
    """

    try:
        resposta = dns.resolver.resolve(dominio, "AAAA")
        return [str(registro) for registro in resposta]

    except dns.resolver.NoAnswer:
        return []

    except dns.resolver.NXDOMAIN:
        return []

    except Exception as erro:
        return [f"Erro: {erro}"]


def exibir_registros(dominio: str, registros_a: List[str], registros_aaaa: List[str]) -> None:
    """
    Exibe no terminal os registros DNS resolvidos para o domínio informado

    Args:
        dominio (str): Nome de domínio consultado
        registros_a (List[str]): Lista de IPs IPv4 resolvidos
        registros_aaaa (List[str]): Lista de IPs IPv6 resolvidos
    """

    print(f"\n{'=' * 60}")
    print("RESOLUÇÃO DNS")
    print(f"{'=' * 60}\n")
    print(f"  Domínio consultado: {dominio}\n")
    print(f"  Registros A (IPv4):")

    if registros_a:
        for ip in registros_a:
            print(f"    {ip}")

    else:
        print("    (nenhum registro encontrado)")

    print(f"\n  Registros AAAA (IPv6):")

    if registros_aaaa:
        for ip in registros_aaaa:
            print(f"    {ip}")

    else:
        print("    (nenhum registro encontrado)")

    print()


def executar_resolucao(dominio: str) -> None:
    """
    Coordena a resolução DNS completa para os tipos A e AAAA e exibe os resultados

    Args:
        dominio (str): Nome de domínio a consultar
    """

    registros_a = resolver_registros_a(dominio)
    registros_aaaa = resolver_registros_aaaa(dominio)
    exibir_registros(dominio, registros_a, registros_aaaa)


executar_resolucao(DOMINIO)
