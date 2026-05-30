import subprocess
import datetime
import time
import sys
from typing import List


TOTAL_CLIENTES = 5
SCRIPT_CLIENTE = "cliente_tcp.py"
PAUSA_ENTRE_saidas = 0.5

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


def lancar_clientes(total: int) -> List[subprocess.Popen]:
    """
    Inicia os processos clientes TCP de forma simultânea via subprocess

    Args:
        total (int): Número de clientes a iniciar

    Returns:
        List[subprocess.Popen]: Lista com os objetos de processo iniciados
    """

    processos = []

    for i in range(1, total + 1):
        registrar(f"Iniciando cliente {i}")
        proc = subprocess.Popen(
            [sys.executable, SCRIPT_CLIENTE, str(i)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processos.append((i, proc))

    return processos


def aguardar_e_exibir(processos: List) -> None:
    """
    Aguarda o término de todos os processos clientes e exibe a saída de cada um

    Args:
        processos (List): Lista de tuplas (id_cliente, Popen) retornada por lancar_clientes
    """

    print(f"\n{'=' * 100}")
    print("SAÍDAS DOS CLIENTES")
    print(f"{'=' * 100}")

    for id_cliente, proc in processos:
        stdout, stderr = proc.communicate(timeout=15)
        codigo = proc.returncode

        print(f"\n--- Cliente {id_cliente} (código de saída: {codigo}) ---\n")

        if stdout.strip():
            for linha in stdout.strip().splitlines():
                print(f"  {linha}")

        if stderr.strip():
            print("  [stderr]")
            for linha in stderr.strip().splitlines():
                print(f"  {linha}")

        registrar(f"Cliente {id_cliente} encerrado com código {codigo}")


def exibir_log() -> None:
    """
    Exibe o log completo da execução ao final do programa
    """

    print(f"\n{'=' * 100}")
    print("LOG DO LANÇADOR")
    print(f"{'=' * 100}\n")

    for entrada in LOG:
        print(f"  {entrada}")

    print()


registrar(f"Lançando {TOTAL_CLIENTES} clientes simultâneos")
processos = lancar_clientes(TOTAL_CLIENTES)
aguardar_e_exibir(processos)
exibir_log()
