import subprocess
import json
import nmap
import re
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime


ALVO_DNS = "zonetransfer.me"
ALVOS_NMAP = ["scanme.nmap.org"]
WORDLIST_SUBDOMAINS = "/usr/share/dnsrecon/subdomains-top1mil-5000.txt"
ARQUIVO_RELATORIO = "relatorio_recon.json"
TOP_PORTAS = 100
TIMEOUT_DNS = 120
TIMEOUT_DNS_BRT = 600
TIMEOUT_NMAP = 300


def executar_dnsrecon_padrao(alvo: str) -> str:
    """
    Executa o dnsrecon para enumerar registros DNS padrao do alvo

    Args:
        alvo (str): Dominio alvo da enumeracao

    Returns:
        str: Saida bruta do dnsrecon em formato texto
    """

    print(f"[*] Enumerando registros DNS padrao de {alvo}...")

    comando = ["dnsrecon", "-d", alvo, "-t", "std"]
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_DNS
    )

    return resultado.stdout + resultado.stderr


def executar_dnsrecon_bruteforce(alvo: str, wordlist: str) -> str:
    """
    Executa o dnsrecon em modo brute force de subdominios utilizando wordlist

    Args:
        alvo (str): Dominio alvo da enumeracao
        wordlist (str): Caminho para o arquivo de wordlist de subdominios

    Returns:
        str: Saida bruta do dnsrecon em formato texto
    """

    if not os.path.exists(wordlist):
        print(f"[AVISO] Wordlist nao encontrada em {wordlist}. Pulando brute force de subdominios.")
        return ""

    print(f"[*] Iniciando brute force de subdominios em {alvo}...")
    comando = ["dnsrecon", "-d", alvo, "-t", "brt", "-D", wordlist]
    print(f"[*] Timeout configurado para {TIMEOUT_DNS_BRT}s. Aguarde...")

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_DNS_BRT
        )
        return resultado.stdout + resultado.stderr

    except subprocess.TimeoutExpired as erro:
        print(f"[AVISO] Brute force encerrado por timeout apos {TIMEOUT_DNS_BRT}s. Aproveitando resultados parciais.")
        saida_parcial = erro.stdout or ""
        stderr_parcial = erro.stderr or ""
        
        if isinstance(saida_parcial, bytes):
            saida_parcial = saida_parcial.decode("utf-8", errors="replace")
        
        if isinstance(stderr_parcial, bytes):
            stderr_parcial = stderr_parcial.decode("utf-8", errors="replace")
        
        return saida_parcial + stderr_parcial


def executar_dnsrecon_axfr(alvo: str) -> str:
    """
    Tenta transferencia de zona AXFR contra o alvo, tecnica classica de reconhecimento

    Args:
        alvo (str): Dominio alvo

    Returns:
        str: Saida bruta do dnsrecon em formato texto
    """

    print(f"[*] Tentando transferencia de zona (AXFR) em {alvo}...")
    comando = ["dnsrecon", "-d", alvo, "-t", "axfr"]
    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_DNS
    )

    return resultado.stdout + resultado.stderr


def parsear_saida_dnsrecon(saida_bruta: str) -> Dict:
    """
    Extrai registros DNS relevantes da saida texto do dnsrecon

    Args:
        saida_bruta (str): Texto completo retornado pelo dnsrecon

    Returns:
        Dict: Dicionario com listas de registros separados por tipo
    """

    registros: Dict = {
        "A": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "AAAA": [],
        "subdominios": [],
        "saida_bruta": saida_bruta
    }

    for linha in saida_bruta.splitlines():
        linha = linha.strip()
        correspondencia_a = re.search(r"\[.\]\s+A\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)", linha)
        
        if correspondencia_a:
            registros["A"].append({
                "host": correspondencia_a.group(1),
                "ip": correspondencia_a.group(2)
            })
        
            if correspondencia_a.group(1) != ALVO_DNS:
                registros["subdominios"].append({
                    "host": correspondencia_a.group(1),
                    "ip": correspondencia_a.group(2)
                })

        correspondencia_mx = re.search(r"\[.\]\s+MX\s+(\S+)\s+(\S+)", linha)
        
        if correspondencia_mx:
            registros["MX"].append({
                "host": correspondencia_mx.group(2),
                "prioridade": correspondencia_mx.group(1)
            })

        correspondencia_ns = re.search(r"\[.\]\s+NS\s+(\S+)\s+(\S+)", linha)
        
        if correspondencia_ns:
            registros["NS"].append({"servidor": correspondencia_ns.group(2)})

        correspondencia_txt = re.search(r"\[.\]\s+TXT\s+\S+\s+(.+)", linha)
        
        if correspondencia_txt:
            registros["TXT"].append({"valor": correspondencia_txt.group(1)})

    return registros


def coletar_ips_unicos(registros_dns: Dict) -> List[str]:
    """
    Extrai todos os enderecos IP unicos descobertos nos registros DNS

    Args:
        registros_dns (Dict): Dicionario de registros retornado por parsear_saida_dnsrecon

    Returns:
        List[str]: Lista de IPs unicos sem duplicatas
    """

    ips = set()

    for entrada in registros_dns.get("A", []):
        ips.add(entrada["ip"])

    return list(ips)


def executar_nmap(hosts: List[str]) -> Dict:
    """
    Varre os hosts informados com deteccao de versao e scripts NSE de vulnerabilidade

    Args:
        hosts (List[str]): Lista de IPs ou hostnames a varrer

    Returns:
        Dict: Resultado estruturado da varredura indexado por host
    """

    scanner = nmap.PortScanner()
    resultados: Dict = {}
    argumentos = f"--top-ports {TOP_PORTAS} -sV --script=vuln,discovery -Pn --host-timeout {TIMEOUT_NMAP}s"

    for host in hosts:
        print(f"[*] Varrendo host: {host}...")

        try:
            scanner.scan(hosts=host, arguments=argumentos)
            resultados[host] = _extrair_resultado_host(scanner, host)

        except nmap.PortScannerError as erro:
            print(f"[ERRO] Falha ao varrer {host}: {erro}")
            resultados[host] = {"erro": str(erro)}

        except Exception as erro:
            print(f"[ERRO] Erro inesperado ao varrer {host}: {erro}")
            resultados[host] = {"erro": str(erro)}

    return resultados


def _extrair_resultado_host(scanner: nmap.PortScanner, host: str) -> Dict:
    """
    Extrai e estrutura os dados de varredura de um host especifico

    Args:
        scanner (nmap.PortScanner): Instancia do scanner com resultados carregados
        host (str): Host cujos dados serao extraidos

    Returns:
        Dict: Dados estruturados do host com status, portas e scripts NSE
    """

    if host not in scanner.all_hosts():
        return {"status": "offline_ou_sem_resposta", "portas": []}

    info_host = scanner[host]
    hostname = ""

    if info_host.hostname():
        hostname = info_host.hostname()

    portas_resultado = []

    for protocolo in info_host.all_protocols():
        for porta in sorted(info_host[protocolo].keys()):
            dados_porta = info_host[protocolo][porta]
            entrada_porta: Dict = {
                "porta": porta,
                "protocolo": protocolo.upper(),
                "status": dados_porta.get("state", ""),
                "servico": dados_porta.get("name", ""),
                "versao": f"{dados_porta.get('product', '')} {dados_porta.get('version', '')}".strip(),
                "scripts_nse": []
            }

            scripts = dados_porta.get("script", {})
            
            for nome_script, saida_script in scripts.items():
                entrada_porta["scripts_nse"].append({
                    "script": nome_script,
                    "saida": saida_script[:500]
                })

            portas_resultado.append(entrada_porta)

    return {
        "hostname": hostname,
        "status": info_host.state(),
        "portas": portas_resultado
    }


def gerar_relatorio(alvo: str, registros_dns: Dict, resultados_nmap: Dict) -> Dict:
    """
    Consolida os dados do DNS e do Nmap em um dicionario de relatorio estruturado

    Args:
        alvo (str): Dominio analisado
        registros_dns (Dict): Resultado do dnsrecon parseado
        resultados_nmap (Dict): Resultado da varredura Nmap por host

    Returns:
        Dict: Relatorio completo com metadata, DNS e varredura
    """

    return {
        "metadata": {
            "alvo": alvo,
            "data_hora": datetime.now().isoformat(),
            "ferramenta": "recon_automation.py"
        },
        "dns": {
            "registros_A": registros_dns.get("A", []),
            "registros_MX": registros_dns.get("MX", []),
            "registros_NS": registros_dns.get("NS", []),
            "registros_TXT": registros_dns.get("TXT", []),
            "subdominios_descobertos": registros_dns.get("subdominios", [])
        },
        "varredura_nmap": resultados_nmap
    }


def salvar_relatorio(relatorio: Dict, caminho: str) -> None:
    """
    Salva o relatorio estruturado em um arquivo JSON

    Args:
        relatorio (Dict): Dicionario com os dados consolidados
        caminho (str): Caminho do arquivo de saida
    """

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)

    print(f"\n[+] Relatorio salvo em: {caminho}")


def exibir_resumo_terminal(alvo: str, registros_dns: Dict, resultados_nmap: Dict) -> None:
    """
    Exibe no terminal um resumo formatado dos resultados de reconhecimento

    Args:
        alvo (str): Dominio analisado
        registros_dns (Dict): Resultado do dnsrecon parseado
        resultados_nmap (Dict): Resultado da varredura Nmap por host
    """

    separador = "=" * 50

    print(f"\n{separador}")
    print("RELATORIO AUTOMATIZADO DE SUPERFICIE DE ATAQUE")
    print(f"{separador}\n")

    print(f"[+] Alvo analisado: {alvo}\n")

    print("[1] RESULTADOS DNS (dnsrecon):")

    for mx in registros_dns.get("MX", []):
        print(f"  Servidor de E-mail (MX): {mx['host']}")

    for ns in registros_dns.get("NS", []):
        print(f"  Servidor DNS (NS): {ns['servidor']}")

    subdominios = registros_dns.get("subdominios", [])
    
    if subdominios:
        print(f"\n  Subdominios descobertos: {len(subdominios)}")
        
        for sub in subdominios[:10]:
            print(f"    * {sub['host']} [IP: {sub['ip']}]")
            
        if len(subdominios) > 10:
            print(f"    ... e mais {len(subdominios) - 10} subdominios (ver relatorio completo)")
            
    else:
        print("  Nenhum subdominio adicional descoberto")

    print(f"\n[2] RESULTADOS DA VARREDURA (Nmap + NSE):")

    for host, dados in resultados_nmap.items():
        print(f"\n  {'-' * 46}")
        hostname = dados.get("hostname", "")
        print(f"  Hospedeiro: {host}" + (f" ({hostname})" if hostname else ""))
        print(f"  {'-' * 46}")

        if "erro" in dados:
            print(f"  [ERRO] {dados['erro']}")
            continue

        portas_abertas = [p for p in dados.get("portas", []) if p["status"] == "open"]

        if not portas_abertas:
            print("  Nenhuma porta aberta encontrada")
            continue

        for porta in portas_abertas:
            versao = porta["versao"] if porta["versao"] else porta["servico"]
            print(f"\n  Porta: {porta['porta']}/{porta['protocolo']} -> Status: OPEN | Servico: {versao}")

            for nse in porta.get("scripts_nse", []):
                linhas = nse["saida"].strip().splitlines()
                resumo = linhas[0] if linhas else ""
                print(f"    [NSE {nse['script']}]: {resumo}")

    print(f"\n{separador}\n")


def executar() -> None:
    """
    Orquestra as etapas de reconhecimento: DNS, varredura Nmap e geracao do relatorio
    """

    print("=" * 50)
    print("   recon_automation.py - Reconhecimento Automatizado")
    print("=" * 50)
    print(f"\n[*] Alvo DNS: {ALVO_DNS}")
    print(f"[*] Alvos Nmap iniciais: {ALVOS_NMAP}\n")

    print("[*] Etapa 1: Reconhecimento DNS\n")

    saida_std = executar_dnsrecon_padrao(ALVO_DNS)
    saida_axfr = executar_dnsrecon_axfr(ALVO_DNS)
    saida_brt = executar_dnsrecon_bruteforce(ALVO_DNS, WORDLIST_SUBDOMAINS)
    saida_completa = saida_std + saida_axfr + saida_brt
    registros_dns = parsear_saida_dnsrecon(saida_completa)

    print(f"[+] Registros A encontrados: {len(registros_dns['A'])}")
    print(f"[+] Subdominios descobertos: {len(registros_dns['subdominios'])}")
    print(f"[+] Registros MX: {len(registros_dns['MX'])}")
    print(f"[+] Registros NS: {len(registros_dns['NS'])}")

    ips_descobertos = coletar_ips_unicos(registros_dns)
    alvos_nmap = list(set(ALVOS_NMAP + ips_descobertos))

    print(f"\n[*] Etapa 2: Varredura Nmap em {len(alvos_nmap)} host(s)\n")
    resultados_nmap = executar_nmap(alvos_nmap)
    relatorio = gerar_relatorio(ALVO_DNS, registros_dns, resultados_nmap)
    salvar_relatorio(relatorio, ARQUIVO_RELATORIO)
    exibir_resumo_terminal(ALVO_DNS, registros_dns, resultados_nmap)
    print(f"[+] Arquivo contendo o log completo salvo em: {ARQUIVO_RELATORIO}")


executar()

