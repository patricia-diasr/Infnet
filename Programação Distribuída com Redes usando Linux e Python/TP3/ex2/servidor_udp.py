import socket
import datetime
from typing import Tuple


HOST = "0.0.0.0"
PORTA = 12345

TAMANHO_BUFFER = 4096

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


def exibir_datagrama(origem: Tuple[str, int], payload: bytes) -> None:
    """
    Exibe no terminal as informações detalhadas de um datagrama recebido

    Args:
        origem  (Tuple[str, int]): Endereço IP e porta de origem do datagrama
        payload (bytes): Conteúdo bruto recebido
    """

    ip_origem = origem[0]
    porta_origem = origem[1]
    tamanho = len(payload)
    conteudo = payload.decode("utf-8", errors="replace")

    print(f"\n  IP de origem: {ip_origem}")
    print(f"  Porta de origem: {porta_origem}")
    print(f"  Tamanho payload: {tamanho} bytes")
    print(f"  Conteúdo: {conteudo[:120]}{'...' if len(conteudo) > 120 else ''}")


def iniciar_servidor() -> None:
    """
    Inicializa o servidor UDP, aguarda datagramas em loop, exibe os dados recebidos e devolve o datagrama ao remetente
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((HOST, PORTA))
        registrar(f"Servidor UDP aguardando datagramas em {HOST}:{PORTA}")

        while True:
            try:
                payload, origem = sock.recvfrom(TAMANHO_BUFFER)
                registrar(f"Datagrama recebido de {origem[0]}:{origem[1]}")
                exibir_datagrama(origem, payload)
                sock.sendto(payload, origem)
                registrar(f"Echo enviado para {origem[0]}:{origem[1]}")

            except OSError as e:
                registrar(f"Erro ao processar datagrama: {e}")

    except OSError as e:
        registrar(f"Erro ao iniciar servidor: {e}")

    except KeyboardInterrupt:
        registrar("Servidor encerrado pelo operador")

    finally:
        sock.close()
        exibir_log()


def exibir_log() -> None:
    """
    Exibe o log completo da execução ao encerrar o servidor
    """

    print(f"\n{'=' * 100}")
    print("LOG DA EXECUÇÃO")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


iniciar_servidor()
