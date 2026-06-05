from typing import List, Tuple


CAPACIDADE_SERVIDOR = 100

VMS_SOLICITADAS = [
    48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
    14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
    44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
    62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
    39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
    60, 24, 46, 16, 22, 51, 30, 8, 40, 25
]


def _ordenar_decrescente(vms: List[int]) -> List[int]:
    """
    Retorna uma nova lista ordenada de forma decrescente usando selection sort

    Args:
        vms (List[int]): Lista de tamanhos de VMs a ordenar

    Returns:
        List[int]: Nova lista ordenada do maior para o menor valor
    """

    lista = list(vms)

    for i in range(len(lista)):
        idx_maior = i

        for j in range(i + 1, len(lista)):
            if lista[j] > lista[idx_maior]:
                idx_maior = j

        lista[i], lista[idx_maior] = lista[idx_maior], lista[i]

    return lista


def next_fit(vms: List[int], capacidade: int) -> List[List[int]]:
    """
    Aloca VMs em servidores usando a heurística Next-Fit

    Args:
        vms (List[int]): Lista de tamanhos de VMs na ordem de chegada
        capacidade (int): Capacidade máxima de RAM de cada servidor

    Returns:
        List[List[int]]: Lista de servidores, cada um contendo as VMs alocadas
    """

    servidores: List[List[int]] = []
    espaco_restante: List[int] = []

    for vm in vms:
        if not servidores or espaco_restante[-1] < vm:
            servidores.append([vm])
            espaco_restante.append(capacidade - vm)

        else:
            servidores[-1].append(vm)
            espaco_restante[-1] -= vm

    return servidores


def first_fit_decreasing(vms: List[int], capacidade: int) -> List[List[int]]:
    """
    Aloca VMs em servidores usando a heurística First-Fit Decreasing

    Args:
        vms (List[int]): Lista de tamanhos de VMs na ordem de chegada
        capacidade (int): Capacidade máxima de RAM de cada servidor

    Returns:
        List[List[int]]: Lista de servidores, cada um contendo as VMs alocadas
    """

    vms_ordenadas = _ordenar_decrescente(vms)

    servidores: List[List[int]] = []
    espaco_restante: List[int] = []

    for vm in vms_ordenadas:
        alocada = False

        for i in range(len(servidores)):
            if espaco_restante[i] >= vm:
                servidores[i].append(vm)
                espaco_restante[i] -= vm
                alocada = True
                break

        if not alocada:
            servidores.append([vm])
            espaco_restante.append(capacidade - vm)

    return servidores


def _calcular_metricas(servidores: List[List[int]], capacidade: int) -> Tuple[int, float, int, int]:
    """
    Calcula métricas de ocupação de um conjunto de servidores alocados

    Args:
        servidores (List[List[int]]): Lista de servidores com as VMs alocadas
        capacidade (int): Capacidade máxima de RAM de cada servidor

    Returns:
        Tuple[int, float, int, int]: Quantidade de servidores, taxa média de ocupação em porcentagem, menor e maior ocupação em GB
    """

    ocupacoes = [sum(s) for s in servidores]
    total_servidores = len(servidores)
    media = sum(ocupacoes) / total_servidores * 100 / capacidade

    return total_servidores, media, min(ocupacoes), max(ocupacoes)


print("\n===== Teste 1 - Heurística Next-Fit =====\n")

servidores_nf = next_fit(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
qtd_nf, media_nf, min_nf, max_nf = _calcular_metricas(servidores_nf, CAPACIDADE_SERVIDOR)

print(f"Servidores utilizados: {qtd_nf}")
print(f"Taxa média de ocupação: {media_nf:.1f}%")
print(f"Menor ocupação: {min_nf} GB  |  Maior ocupação: {max_nf} GB\n")

for i, servidor in enumerate(servidores_nf, 1):
    total = sum(servidor)
    print(f"Servidor {i:>2}: {servidor}  (Total: {total}/{CAPACIDADE_SERVIDOR} GB)")


print("\n\n===== Teste 2 - Heurística First-Fit Decreasing =====\n")

servidores_ffd = first_fit_decreasing(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
qtd_ffd, media_ffd, min_ffd, max_ffd = _calcular_metricas(servidores_ffd, CAPACIDADE_SERVIDOR)

print(f"Servidores utilizados: {qtd_ffd}")
print(f"Taxa média de ocupação: {media_ffd:.1f}%")
print(f"Menor ocupação: {min_ffd} GB  |  Maior ocupação: {max_ffd} GB\n")

for i, servidor in enumerate(servidores_ffd, 1):
    total = sum(servidor)
    print(f"Servidor {i:>2}: {servidor}  (Total: {total}/{CAPACIDADE_SERVIDOR} GB)")


print("\n\n===== Teste 3 - Relatório Comparativo =====\n")

print("=== RESULTADO DA ALOCAÇÃO (HEURÍSTICAS) ===\n")

print("[Heurística Next-Fit]")
print(f"Servidores utilizados: {qtd_nf} servidores")
exemplo_nf = servidores_nf[0]
print(f"Exemplo de ocupação do Servidor 1: {exemplo_nf} (Total: {sum(exemplo_nf)}/{CAPACIDADE_SERVIDOR} GB)\n")

print("[Heurística First-Fit Decreasing]")
print(f"Servidores utilizados: {qtd_ffd} servidores")
exemplo_ffd = servidores_ffd[0]
print(f"Exemplo de ocupação do Servidor 1: {exemplo_ffd} (Total: {sum(exemplo_ffd)}/{CAPACIDADE_SERVIDOR} GB)\n")
economia = qtd_nf - qtd_ffd

if economia > 0:
    print(f"Conclusão: A heurística First-Fit Decreasing economizou {economia} servidor(es) em relação à Next-Fit")

elif economia == 0:
    print("Conclusão: Ambas as heurísticas utilizaram o mesmo número de servidores")

else:
    print(f"Conclusão: A heurística Next-Fit utilizou {-economia} servidor(es) a menos que a First-Fit Decreasing")


print("\n\n===== Teste 4 - Verificação de Integridade =====\n")

total_ram_original = sum(VMS_SOLICITADAS)
total_ram_nf = sum(sum(s) for s in servidores_nf)
total_ram_ffd = sum(sum(s) for s in servidores_ffd)
total_vms_nf = sum(len(s) for s in servidores_nf)
total_vms_ffd = sum(len(s) for s in servidores_ffd)

print(f"Total de VMs na entrada: {len(VMS_SOLICITADAS)}")
print(f"Total de RAM solicitada: {total_ram_original} GB\n")
print(f"Next-Fit           VMs alocadas: {total_vms_nf}  |  RAM alocada: {total_ram_nf} GB  |  Íntegro: {total_ram_nf == total_ram_original}")
print(f"First-Fit Dec.     VMs alocadas: {total_vms_ffd}  |  RAM alocada: {total_ram_ffd} GB  |  Íntegro: {total_ram_ffd == total_ram_original}\n")
