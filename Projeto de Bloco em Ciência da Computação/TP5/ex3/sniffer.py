import pcapy
import struct


INTERFACE = "enp0s3"
PORTA_ALVO = 8443
FILTRO_BPF = f"tcp port {PORTA_ALVO}"
TAMANHO_SNAPSHOT = 65536
MODO_PROMISCUO = 1
TIMEOUT_MS = 1000
PADROES_SUSPEITOS = ["AUTH_TOKEN", "REBOOT_SERVER", "CMD"]


def _extrair_payload_ip(pacote: bytes) -> bytes:
    """
    Extrai o payload apos o cabecalho Ethernet e IP de um pacote capturado

    Args:
        pacote (bytes): Bytes brutos do pacote capturado

    Returns:
        bytes: Bytes do payload TCP, ou sequencia vazia se o pacote for curto demais
    """

    if len(pacote) < 14:
        return b""

    cabecalho_eth = 14
    dados_ip = pacote[cabecalho_eth:]

    if len(dados_ip) < 20:
        return b""

    ihl = (dados_ip[0] & 0x0F) * 4
    dados_tcp = dados_ip[ihl:]

    if len(dados_tcp) < 20:
        return b""

    offset_dados = ((dados_tcp[12] >> 4) & 0xF) * 4
    payload = dados_tcp[offset_dados:]

    return payload


def _converter_para_texto(payload: bytes) -> str:
    """
    Converte bytes brutos em string, substituindo caracteres nao imprimiveis por ponto

    Args:
        payload (bytes): Bytes do payload a converter

    Returns:
        str: String com caracteres imprimiveis preservados e demais substituidos por ponto
    """

    return "".join(chr(b) if 32 <= b < 127 else "." for b in payload)


def _inspecionar_pacote(cabecalho, pacote: bytes) -> None:
    """
    Processa um pacote capturado, exibe seu conteudo e busca por padroes suspeitos

    Args:
        cabecalho: Objeto de cabecalho retornado pelo pcapy com metadados do pacote
        pacote (bytes): Bytes brutos do pacote capturado
    """

    tamanho = cabecalho.getlen()
    print(f"\n[+] Pacote TCP Capturado! Tamanho: {tamanho} bytes")
    payload = _extrair_payload_ip(pacote)

    if not payload:
        print("    Payload vazio ou pacote de controle TCP (SYN/ACK/FIN)")
        return

    hex_bruto = payload.hex()
    print(f"[Dados Brutos do Payload]: {' '.join(hex_bruto[i:i+2] for i in range(0, min(len(hex_bruto), 60), 2))}...")
    texto = _converter_para_texto(payload)
    print(f"[Texto Convertido]: {texto[:80]}...")
    encontrado = False
    
    for padrao in PADROES_SUSPEITOS:
        if padrao in texto or padrao.encode() in payload:
            print(f"[!!!] ALERTA CRITICO: Padrao '{padrao}' encontrado em texto claro! COMUNICACAO NAO ESTA CIFRADA!")
            encontrado = True

    if not encontrado:
        for padrao in PADROES_SUSPEITOS:
            print(f"[-] Alerta: Padrao '{padrao}' NAO encontrado. Os dados estao devidamente cifrados via TLS")


def iniciar_captura() -> None:
    """
    Abre a interface de rede, aplica filtro BPF e inicia o loop de captura de pacotes
    """

    print(f"[*] Iniciando captura na interface {INTERFACE} (Porta {PORTA_ALVO})...")
    print(f"[*] Filtro BPF aplicado: '{FILTRO_BPF}'")
    print(f"[*] Padroes monitorados: {PADROES_SUSPEITOS}")
    print("[*] Aguardando pacotes... (Ctrl+C para encerrar)\n")

    capturador = pcapy.open_live(INTERFACE, TAMANHO_SNAPSHOT, MODO_PROMISCUO, TIMEOUT_MS)
    capturador.setfilter(FILTRO_BPF)

    while True:
        cabecalho, pacote = capturador.next()
        
        if cabecalho is not None:
            _inspecionar_pacote(cabecalho, pacote)

try:
    iniciar_captura()
except KeyboardInterrupt:
    print("\n[*] Captura encerrada pelo usuario")

