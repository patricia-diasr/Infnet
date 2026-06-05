from scapy.all import ARP, Ether, srp, sniff, conf
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import ipaddress


REDE_ALVO = "192.168.56.0/24"
IP_GATEWAY = "192.168.56.1"
TIMEOUT_SCAN = 2
LIMITE_IPS_POR_MAC = 3
INTERFACE = "enp0s3"


def escanear_rede(rede: str, timeout: int) -> Dict[str, str]:
    """
    Envia ARP Requests para toda a faixa de rede e mapeia os dispositivos que respondem

    Args:
        rede (str): Faixa de rede em notação CIDR, ex: 192.168.1.0/24
        timeout (int): Tempo de espera em segundos por respostas ARP

    Returns:
        Dict[str, str]: Dicionário mapeando IP para MAC de cada dispositivo ativo encontrado
    """

    print(f"\n[*] Iniciando scan da rede {rede}...")
    print(f"[*] Timeout por resposta: {timeout}s\n")

    pacote_arp = ARP(pdst=rede)
    frame_broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    pacote = frame_broadcast / pacote_arp

    conf.verb = 0
    respondidos, _ = srp(pacote, timeout=timeout, iface=INTERFACE)
    tabela_verdade: Dict[str, str] = {}

    for _, resposta in respondidos:
        ip = resposta[ARP].psrc
        mac = resposta[ARP].hwsrc
        tabela_verdade[ip] = mac

    return tabela_verdade


def exibir_tabela_verdade(tabela: Dict[str, str]) -> None:
    """
    Exibe a tabela de mapeamento IP-MAC coletada pelo scanner

    Args:
        tabela (Dict[str, str]): Dicionário de IP para MAC
    """

    print(f"{'IP':<18}  {'MAC':<20}  {'Observação'}")
    print(f"{'-'*18}  {'-'*20}  {'-'*20}")

    for ip, mac in sorted(tabela.items(), key=lambda x: ipaddress.ip_address(x[0])):
        obs = "GATEWAY" if ip == IP_GATEWAY else ""
        print(f"{ip:<18}  {mac:<20}  {obs}")

    print(f"\nTotal de dispositivos ativos: {len(tabela)}\n")



class DetectorArpSpoofing:
    """
    Monitora pacotes ARP em tempo real e detecta tentativas de spoofing

    Attributes:
        tabela_verdade (Dict[str, str]): Mapeamento IP-MAC legítimo coletado no scan inicial
        mac_gateway (Optional[str]): MAC legítimo do gateway, extraído da tabela verdade
        alertas (List[str]): Histórico de alertas emitidos durante o monitoramento
        macs_para_ips (Dict[str, List[str]]): Rastreia quais IPs cada MAC respondeu
        contagem_pacotes (int): Total de pacotes ARP inspecionados desde o início
    """

    def __init__(self, tabela_verdade: Dict[str, str]) -> None:
        self.tabela_verdade: Dict[str, str] = tabela_verdade
        self.mac_gateway: Optional[str] = tabela_verdade.get(IP_GATEWAY)
        self.alertas: List[str] = []
        self.macs_para_ips: Dict[str, List[str]] = {}
        self.contagem_pacotes: int = 0

    def inspecionar_pacote(self, pacote) -> None:
        """
        Callback chamado pelo sniffer para cada pacote ARP capturado

        Args:
            pacote: Pacote Scapy capturado pelo sniff
        """

        if not pacote.haslayer(ARP):
            return

        camada_arp = pacote[ARP]

        if camada_arp.op != 2:
            return

        self.contagem_pacotes += 1
        ip_anunciado = camada_arp.psrc
        mac_anunciado = camada_arp.hwsrc
        self._rastrear_mac(mac_anunciado, ip_anunciado)
        self._verificar_spoofing_gateway(ip_anunciado, mac_anunciado)
        self._verificar_mac_multiplos_ips(mac_anunciado)

    def _verificar_spoofing_gateway(self, ip_anunciado: str, mac_anunciado: str) -> None:
        """
        Verifica se algum dispositivo está anunciando o IP do gateway com um MAC diferente do legítimo

        Args:
            ip_anunciado (str): IP contido no ARP Reply inspecionado
            mac_anunciado (str): MAC contido no ARP Reply inspecionado
        """

        if ip_anunciado != IP_GATEWAY:
            return

        if self.mac_gateway is None:
            self._registrar_alerta(
                "AVISO",
                f"ARP Reply para o IP do gateway {IP_GATEWAY} detectado, "
                f"mas o gateway não estava na tabela inicial. MAC anunciado: {mac_anunciado}"
            )
            return

        if mac_anunciado != self.mac_gateway:
            self._registrar_alerta(
                "CRÍTICO",
                f"ARP SPOOFING DETECTADO no gateway {IP_GATEWAY} | "
                f"MAC legítimo: {self.mac_gateway} | "
                f"MAC falso anunciado: {mac_anunciado}"
            )

    def _verificar_mac_multiplos_ips(self, mac: str) -> None:
        """
        Verifica se um mesmo MAC respondeu por mais IPs do que o limite permitido

        Args:
            mac (str): Endereço MAC a ser avaliado
        """

        ips_do_mac = self.macs_para_ips.get(mac, [])

        if len(ips_do_mac) > LIMITE_IPS_POR_MAC:
            self._registrar_alerta(
                "SUSPEITO",
                f"MAC {mac} respondeu por {len(ips_do_mac)} IPs distintos: {ips_do_mac}"
            )

    def _rastrear_mac(self, mac: str, ip: str) -> None:
        """
        Registra a associação entre um MAC e um IP para rastreamento histórico

        Args:
            mac (str): Endereço MAC observado
            ip (str): Endereço IP anunciado por esse MAC
        """

        if mac not in self.macs_para_ips:
            self.macs_para_ips[mac] = []

        if ip not in self.macs_para_ips[mac]:
            self.macs_para_ips[mac].append(ip)

    def _registrar_alerta(self, nivel: str, mensagem: str) -> None:
        """
        Registra e exibe um alerta de segurança com timestamp

        Args:
            nivel (str): Nível de severidade do alerta, ex: CRÍTICO, SUSPEITO, AVISO
            mensagem (str): Descrição detalhada do evento detectado
        """

        timestamp = datetime.now().strftime("%H:%M:%S")
        alerta = f"[{timestamp}] [{nivel}] {mensagem}"
        self.alertas.append(alerta)
        print(f"\n{'!'*60}")
        print(alerta)
        print(f"{'!'*60}\n")

    def exibir_resumo(self) -> None:
        """
        Exibe o resumo final do monitoramento com estatísticas e histórico de alertas
        """

        print("\n===== Resumo do Monitoramento =====\n")
        print(f"Pacotes ARP Reply inspecionados: {self.contagem_pacotes}")
        print(f"Total de alertas emitidos: {len(self.alertas)}")
        print(f"MACs distintos observados: {len(self.macs_para_ips)}\n")

        if self.alertas:
            print("Histórico de alertas:")
            for alerta in self.alertas:
                print(f"  {alerta}")
        else:
            print("Nenhum comportamento suspeito detectado durante o monitoramento")

        print()


def executar() -> None:
    """
    Coordena as duas etapas: scan inicial da rede e monitoramento contínuo de ARP Spoofing
    """

    print("=" * 60)
    print("   Ferramenta de Auditoria ARP - Detector de MitM")
    print("=" * 60)

    tabela = escanear_rede(REDE_ALVO, TIMEOUT_SCAN)

    if not tabela:
        print("[ERRO] Nenhum dispositivo encontrado. Verifique a interface e a faixa de rede.")
        return

    print("\n===== Tabela Verdade da Rede =====\n")
    exibir_tabela_verdade(tabela)

    if IP_GATEWAY not in tabela:
        print(f"[AVISO] Gateway {IP_GATEWAY} não respondeu ao scan. A detecção de spoofing do gateway ficará comprometida.\n")
    else:
        print(f"[*] MAC legítimo do gateway registrado: {tabela[IP_GATEWAY]}\n")

    detector = DetectorArpSpoofing(tabela)

    print(f"[*] Iniciando monitoramento de ARP Spoofing na interface {INTERFACE}...")
    print("[*] Pressione Ctrl+C para encerrar e exibir o resumo\n")

    try:
        sniff(
            iface=INTERFACE,
            filter="arp",
            prn=detector.inspecionar_pacote,
            store=False
        )

    except KeyboardInterrupt:
        detector.exibir_resumo()


executar()
