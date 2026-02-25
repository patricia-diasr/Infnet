from typing import List, Tuple
import random
import time

def maior_unico_quadratico(lista: List[int]) -> Tuple[int, int]:
    """
    Encontra o maior número único em uma lista utilizando dois laços aninhados e conta número total de comparações realizadas

    Args:
        lista (List[int]): Lista de números inteiros

    Returns:
        Tuple[int, int]:
            - Maior número único encontrado (ou None se não houver)
            - Número total de comparações realizadas
    """

    comparacoes = 0
    maior_unico = None

    for i in range(len(lista)):
        contador = 0

        for j in range(len(lista)):
            comparacoes += 1
            if lista[i] == lista[j]:
                contador += 1

        if contador == 1:
            if maior_unico is None or lista[i] > maior_unico:
                maior_unico = lista[i]

    return maior_unico, comparacoes
    
    
def maior_unico_hash(lista: List[int]) -> Tuple[int, int]:
    """
    Encontra o maior número único utilizando uma hash table (dict), e conta número total de acessos à estrutura

    Args:
        lista (List[int]): Lista de números inteiros

    Returns:
        Tuple[int, int]:
            - Maior número único encontrado (ou None se não houver)
            - Número total de acessos à estrutura
    """

    acessos = 0
    frequencias = {}

    for numero in lista:
        acessos += 1  
        if numero in frequencias:
            frequencias[numero] += 1
        else:
            frequencias[numero] = 1

    maior_unico = None

    for numero, contagem in frequencias.items():
        acessos += 1
        if contagem == 1:
            if maior_unico is None or numero > maior_unico:
                maior_unico = numero

    return maior_unico, acessos


tamanhos_lista = [5, 10, 25, 50, 100, 300, 500]

total_comparacoes_quadratico = 0
total_tempo_quadratico = 0

total_acessos_hash = 0
total_tempo_hash = 0

for tamanho in tamanhos_lista:
    lista = [random.randint(0, tamanho // 2) for _ in range(tamanho)]

    print(f"\n===== Lista com {tamanho} elementos =====")
    print("\nLista:", lista)

    inicio = time.perf_counter()
    resultado_quadratico, comparacoes_quadratico = maior_unico_quadratico(lista)
    fim = time.perf_counter()
    
    tempo_q = fim - inicio
    total_comparacoes_quadratico += comparacoes_quadratico
    total_tempo_quadratico += tempo_q
    
    print("\nVersão Quadrática:")
    print(f"Maior único: {resultado_quadratico}")
    print(f"Comparações: {comparacoes_quadratico}")
    print(f"Tempo: {tempo_q:.6f} segundos")

    inicio = time.perf_counter()
    resultado_hash, acessos_hash = maior_unico_hash(lista)
    fim = time.perf_counter()
    
    tempo_h = fim - inicio
    total_acessos_hash += acessos_hash
    total_tempo_hash += tempo_h
    
    print("\nVersão com Hash Table:")
    print(f"Maior único: {resultado_hash}")
    print(f"Acessos realizados: {acessos_hash}")
    print(f"Tempo: {tempo_h:.6f} segundos")


print("\n ===== Eficiência Total =====")

print("\nVersão Quadrática:")
print(f"Total de comparações: {total_comparacoes_quadratico}")
print(f"Tempo total acumulado: {total_tempo_quadratico:.6f} segundos")

print("\nVersão com Hash Table:")
print(f"Total de acessos: {total_acessos_hash}")
print(f"Tempo total acumulado: {total_tempo_hash:.6f} segundos")
