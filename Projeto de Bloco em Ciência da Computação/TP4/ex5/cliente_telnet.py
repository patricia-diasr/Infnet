import socket
import time
import datetime
from typing import List, Tuple


HOST_SERVIDOR = "192.168.56.101"
PORTA = 23
TIMEOUT = 5
PAUSA_ENTRE_COMANDOS = 1.5
TAMANHO_BUFFER = 4096

COMANDOS_TESTE: List[Tuple[str, str]] = [
    ("hostname",  "Nome da máquina remota"),
    ("data", "Data atual no servidor"),
    ("hora", "Hora atual no servidor"),
    ("quem", "Usuário logado no servidor"),
    ("uptime", "Tempo de atividade do servidor"),
    ("memoria", "Uso de memória RAM"),
    ("disco", "Uso de disco"),
    ("processos", "Processos ativos por CPU"),
    ("rede", "Interfaces de rede"),
    ("ajuda", "Listagem de comandos"),
    ("invalido", "Comando não reconhecido (teste de erro)"),
]

LOG_SESSAO: list = []


def registrar(evento: str) -> None:
    """
    Registra um evento com timestamp no log da sessão

    Args:
        evento (str): Descrição do evento
    """

    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {evento}"
    LOG_SESSAO.append(entrada)
    print(entrada)


def responder_negociacao(dados: bytes) -> bytes:
    """
    Analisa os bytes recebidos e gera respostas para sequências IAC de negociação

    Args:
        dados (bytes): Bytes brutos recebidos do servidor

    Returns:
        bytes: Bytes de resposta às negociações IAC encontradas
    """

    resposta = bytearray()
    i = 0

    while i < len(dados):
        if dados[i] == 255 and i + 2 < len(dados):
            comando = dados[i + 1]
            opcao   = dados[i + 2]

            if comando == 253:
                resposta += bytes([255, 252, opcao])

            elif comando == 251:
                resposta += bytes([255, 254, opcao])

            i += 3

        else:
            i += 1

    return bytes(resposta)


def limpar_iac(dados: bytes) -> str:
    """
    Remove todas as sequências IAC e caracteres de controle dos dados recebidos

    Args:
        dados (bytes): Bytes brutos com possíveis sequências de protocolo Telnet

    Returns:
        str: Texto legível sem sequências de controle
    """

    resultado = bytearray()
    i = 0

    while i < len(dados):
        if dados[i] == 255:
            if i + 2 < len(dados):
                i += 3

            else:
                i += 1

        elif dados[i] not in (0, 13):
            resultado.append(dados[i])
            i += 1

        else:
            i += 1

    return resultado.decode("utf-8", errors="ignore")


def executar_sessao_telnet() -> List[Tuple[str, str, str]]:
    """
    Abre uma sessão Telnet com socket puro, negocia as opções IAC, executa todos os comandos de teste e coleta as respostas

    Returns:
        List[Tuple[str, str, str]]: Lista de tuplas (comando, descrição, resposta)
    """

    resultados: List[Tuple[str, str, str]] = []

    try:
        registrar(f"Conectando ao servidor {HOST_SERVIDOR}:{PORTA}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((HOST_SERVIDOR, PORTA))
        registrar("Conexão TCP estabelecida")

        time.sleep(0.5)
        dados_iniciais = sock.recv(TAMANHO_BUFFER)
        respostas_iac = responder_negociacao(dados_iniciais)

        if respostas_iac:
            sock.sendall(respostas_iac)
            registrar(f"Negociação IAC concluída ({len(respostas_iac)} bytes enviados)")

        time.sleep(0.5)

        try:
            sock.recv(TAMANHO_BUFFER)

        except socket.timeout:
            pass

        for comando, descricao in COMANDOS_TESTE:
            registrar(f"Enviando comando: '{comando}'")
            sock.sendall((comando + "\n").encode("utf-8"))
            time.sleep(PAUSA_ENTRE_COMANDOS)
            resposta_bruta = b""

            try:
                while True:
                    sock.settimeout(0.4)
                    fragmento = sock.recv(TAMANHO_BUFFER)

                    if not fragmento:
                        break

                    resposta_bruta += fragmento

            except socket.timeout:
                pass

            sock.settimeout(TIMEOUT)
            resposta = limpar_iac(resposta_bruta).strip()
            resposta = " | ".join(
                linha.strip()
                for linha in resposta.splitlines()
                if linha.strip() and linha.strip() != "$"
            )

            registrar(f"Resposta recebida ({len(resposta)} caracteres)")
            resultados.append((comando, descricao, resposta[:80]))

        registrar("Enviando comando de encerramento")
        sock.sendall(b"sair\n")
        time.sleep(0.5)
        sock.close()
        registrar("Sessão encerrada com sucesso")

    except ConnectionRefusedError:
        registrar(f"Erro: conexão recusada em {HOST_SERVIDOR}:{PORTA}")

    except socket.timeout:
        registrar("Erro: timeout ao conectar ao servidor")

    except Exception as e:
        registrar(f"Erro inesperado: {e}")

    return resultados


def exibir_tabela(resultados: List[Tuple[str, str, str]]) -> None:
    """
    Exibe os resultados dos testes em formato tabular

    Args:
        resultados (List[Tuple[str, str, str]]): Lista de (comando, descrição, resposta)
    """

    col_n = 4
    col_cmd = 12
    col_desc = 35
    col_resp = 50

    sep = f"+{'-' * (col_n + 2)}+{'-' * (col_cmd + 2)}+{'-' * (col_desc + 2)}+{'-' * (col_resp + 2)}+"
    cab = (f"| {'#':^{col_n}} | {'Comando':^{col_cmd}} | {'Descrição':^{col_desc}} | {'Resposta (resumida)':^{col_resp}} |")

    print("\n===== Resultados da sessão Telnet =====\n")
    print(sep)
    print(cab)
    print(sep)

    for i, (cmd, desc, resp) in enumerate(resultados, 1):
        print(f"| {str(i):^{col_n}} | {cmd:<{col_cmd}} | {desc:<{col_desc}} | {resp:<{col_resp}} |")

    print(sep)


def exibir_log() -> None:
    """
    Exibe o log completo da sessão ao final da execução
    """

    print("\n===== Log da sessão =====\n")

    for entrada in LOG_SESSAO:
        print(f"  {entrada}")

    print()


resultados = executar_sessao_telnet()
exibir_tabela(resultados)
exibir_log()
