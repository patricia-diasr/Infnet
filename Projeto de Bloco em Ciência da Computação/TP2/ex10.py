import asyncio
import random


async def sensor_cardiaco(fila: asyncio.Queue, duracao: int) -> None:
    """
    Corrotina produtora que gera batimentos cardíacos aleatórios e os coloca na fila

    Args:
        fila (asyncio.Queue): Fila compartilhada onde os batimentos serão inseridos
        duracao (int): Tempo total em segundos que o sensor ficará ativo
    """

    fim = asyncio.get_event_loop().time() + duracao

    while asyncio.get_event_loop().time() < fim:
        batimento = random.randint(40, 180)
        await fila.put(batimento)

        print(f"[Sensor] Batimento gerado: {batimento} bpm")
        await asyncio.sleep(0.5)


async def monitor_medico(fila: asyncio.Queue, duracao: int) -> None:
    """
    Corrotina consumidora que analisa os batimentos cardíacos retirados da fila

    Args:
        fila (asyncio.Queue): Fila compartilhada de onde os batimentos serão retirados
        duracao (int): Tempo total em segundos que o monitor ficará ativo
    """

    fim = asyncio.get_event_loop().time() + duracao

    while asyncio.get_event_loop().time() < fim:
        try:
            batimento = await asyncio.wait_for(fila.get(), timeout=1.0)

            if batimento > 120:
                print(f"[Monitor] ⚠️ ALERTA: Batimento em {batimento}!")

            else:
                print(f"[Monitor] ✅ Normal: {batimento}")

            fila.task_done()

        except asyncio.TimeoutError:
            continue


async def executar_sistema(duracao: int) -> None:
    """
    Inicializa e gerencia o ciclo de vida do sistema produtor-consumidor

    Args:
        duracao (int): Tempo total em segundos que o sistema ficará em execução
    """

    fila: asyncio.Queue = asyncio.Queue(maxsize=10)

    produtor = asyncio.create_task(sensor_cardiaco(fila, duracao))
    consumidor = asyncio.create_task(monitor_medico(fila, duracao))

    await asyncio.gather(produtor, consumidor)


print("===== Teste 1 - Sistema de Monitoramento Cardíaco =====\n")
print("Duração: 10 segundos | Fila máxima: 10 | Alerta acima de: 120 bpm\n")
print("=" * 45 + "\n")

asyncio.run(executar_sistema(duracao=10))

print("\n" + "=" * 45)
print("  Sistema encerrado com sucesso")
