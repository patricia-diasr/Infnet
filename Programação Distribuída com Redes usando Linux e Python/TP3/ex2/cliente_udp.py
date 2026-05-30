import socket
import random
import string
import datetime
import time
from typing import List, Dict, Tuple


HOST_SERVIDOR = "192.168.56.101"
PORTA = 12345

TOTAL_MENSAGENS = 10
TAMANHO_MINIMO = 10
TAMANHO_MAXIMO = 2000
TAMANHO_BUFFER = 4096
TIMEOUT_RESPOSTA = 3.0
PAUSA_ENTRE_ENVIOS = 0.2

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


def gerar_conteudo(tamanho: int) -> str:
    """
    Gera uma string aleatória de letras e dígitos com o comprimento solicitado

    Args:
        tamanho (int): Quantidade de caracteres a gerar

    Returns:
        str: String aleatória com exatamente tamanho caracteres
    """

    caracteres = string.ascii_letters + string.digits
    return "".join(random.choices(caracteres, k=tamanho))


def montar_mensagem(id_sequencia: int) -> Tuple[str, int]:
    """
    Monta a mensagem no formato ID + separador + conteúdo com tamanho aleatório

    Args:
        id_sequencia (int): Número de sequência da mensagem

    Returns:
        Tuple[str, int]: Mensagem formatada e tamanho do conteúdo gerado
    """

    tamanho = random.randint(TAMANHO_MINIMO, TAMANHO_MAXIMO)
    conteudo = gerar_conteudo(tamanho)
    mensagem = f"{id_sequencia} - {conteudo}"
    return mensagem, tamanho


def enviar_mensagens(sock: socket.socket) -> List[Dict]:
    """
    Envia as mensagens ao servidor e aguarda o echo de cada uma, registrando os resultados

    Args:
        sock (socket.socket): Socket UDP já configurado com timeout

    Returns:
        List[Dict]: Lista de dicionários com os dados de cada envio
    """

    resultados = []

    for i in range(1, TOTAL_MENSAGENS + 1):
        mensagem, tamanho_conteudo = montar_mensagem(i)
        payload = mensagem.encode("utf-8")

        registrar(f"Enviando mensagem {i:02d} ({len(payload)} bytes)")

        try:
            sock.sendto(payload, (HOST_SERVIDOR, PORTA))
            t_envio = datetime.datetime.now()

            try:
                echo, origem = sock.recvfrom(TAMANHO_BUFFER)
                t_retorno = datetime.datetime.now()
                latencia_ms = (t_retorno - t_envio).total_seconds() * 1000
                eco_correto = echo == payload

                registrar(f"  Echo recebido de {origem[0]}:{origem[1]}  latencia={latencia_ms:.2f}ms  integro={'sim' if eco_correto else 'nao'}")

                resultados.append({
                    "id": i,
                    "bytes_enviados": len(payload),
                    "tamanho_conteudo": tamanho_conteudo,
                    "echo_recebido": True,
                    "echo_integro": eco_correto,
                    "latencia_ms": round(latencia_ms, 2),
                })

            except socket.timeout:
                registrar(f"  Timeout: echo nao recebido para mensagem {i:02d}")

                resultados.append({
                    "id": i,
                    "bytes_enviados": len(payload),
                    "tamanho_conteudo": tamanho_conteudo,
                    "echo_recebido": False,
                    "echo_integro": False,
                    "latencia_ms": None,
                })

        except OSError as e:
            registrar(f"  Erro ao enviar mensagem {i:02d}: {e}")

            resultados.append({
                "id": i,
                "bytes_enviados": len(payload),
                "tamanho_conteudo": tamanho_conteudo,
                "echo_recebido": False,
                "echo_integro": False,
                "latencia_ms": None,
            })

        time.sleep(PAUSA_ENTRE_ENVIOS)

    return resultados


def exibir_tabela(resultados: List[Dict]) -> None:
    """
    Exibe os resultados dos envios em formato tabular

    Args:
        resultados (List[Dict]): Lista retornada por enviar_mensagens
    """

    col_id = 4
    col_bytes = 14
    col_conteud = 16
    col_echo = 8
    col_integro = 8
    col_latenci = 14

    sep = (f"+{'-' * (col_id + 2)}+{'-' * (col_bytes + 2)}+{'-' * (col_conteud + 2)}+{'-' * (col_echo + 2)}+{'-' * (col_integro + 2)}+{'-' * (col_latenci + 2)}+")

    cab = (f"| {'#':^{col_id}} | {'Bytes enviados':^{col_bytes}} | {'Tam. conteúdo':^{col_conteud}} | {'Echo':^{col_echo}} | {'Íntegro':^{col_integro}} | {'Latência (ms)':^{col_latenci}} |")

    print(f"\n{'=' * 100}")
    print("RESULTADOS DO CLIENTE UDP")
    print(f"{'=' * 100}\n")
    print(sep)
    print(cab)
    print(sep)

    for r in resultados:
        echo = "Sim" if r["echo_recebido"] else "Não"
        integro = "Sim" if r["echo_integro"]  else ("Não" if r["echo_recebido"] else "-")
        latenci = f"{r['latencia_ms']:.2f}" if r["latencia_ms"] is not None else "-"

        print(f"| {str(r['id']):^{col_id}} | {str(r['bytes_enviados']):^{col_bytes}} | {str(r['tamanho_conteudo']):^{col_conteud}} | {echo:^{col_echo}} | {integro:^{col_integro}} | {latenci:^{col_latenci}} |")

    print(sep)

    total = len(resultados)
    recebidos = sum(1 for r in resultados if r["echo_recebido"])
    perdidos = total - recebidos
    integros = sum(1 for r in resultados if r["echo_integro"])
    latencias = [r["latencia_ms"] for r in resultados if r["latencia_ms"] is not None]
    media_lat = sum(latencias) / len(latencias) if latencias else 0

    print(f"\n  Mensagens enviadas: {total}")
    print(f"  Echos recebidos: {recebidos}")
    print(f"  Perdas: {perdidos}")
    print(f"  Íntegros: {integros}")
    print(f"  Latência média: {media_lat:.2f} ms")


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


def executar_cliente() -> None:
    """
    Inicializa o socket UDP, executa os envios e exibe os resultados
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TIMEOUT_RESPOSTA)

        registrar(f"Cliente UDP iniciado, alvo: {HOST_SERVIDOR}:{PORTA}")
        resultados = enviar_mensagens(sock)
        exibir_tabela(resultados)

    except OSError as e:
        registrar(f"Erro ao criar socket: {e}")

    finally:
        sock.close()
        registrar("Socket encerrado")
        exibir_log()


executar_cliente()
