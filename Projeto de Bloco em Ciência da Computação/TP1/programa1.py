import time
import random
from typing import List, Tuple, Callable, Dict


def ler_listagem_arquivos(caminho_arquivo: str) -> List[str]:
    """Lê um arquivo de texto contendo a listagem de arquivos

    Args:
        caminho_arquivo (str): Caminho para o arquivo de texto

    Returns:
        List[str]: Lista contendo os nomes dos arquivos
    """
    
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]


def bubble_sort(lista: List[str]) -> Tuple[List[str], int]:
    """Ordena uma lista utilizando Bubble Sort e contabiliza os passos

    Args:
        lista (List[str]): Lista a ser ordenada

    Returns:
        Tuple[List[str], int]: 
            - Lista ordenada 
            - Quantidade de passos executados
    """
    
    lista_ordenada = lista.copy()
    tamanho = len(lista_ordenada)
    passos = 0

    for i in range(tamanho):
        passos += 2  # controle do loop externo + atribuição da variável trocou
        trocou = False
        
        for j in range(0, tamanho - i - 1):
            passos += 2  # controle do loop interno + comparação
            
            if lista_ordenada[j] > lista_ordenada[j + 1]:
                passos += 5  # entrada no bloco condicional + troca realizada (duas atribuições + operação de swap) + atribuição da variável trocou

                lista_ordenada[j], lista_ordenada[j + 1] = (
                    lista_ordenada[j + 1],
                    lista_ordenada[j],
                )
                trocou = True

        passos += 1  # verificação do if not trocou
        if not trocou:
            passos += 1  # entrada no break
            break
                
    return lista_ordenada, passos


def selection_sort(lista: List[str]) -> Tuple[List[str], int]:
    """Ordena uma lista utilizando Selection Sort e contabiliza os passos

    Args:
        lista (List[str]): Lista a ser ordenada

    Returns:
        Tuple[List[str], int]: 
            - Lista ordenada 
            - Quantidade de passos executados
    """
    
    lista_ordenada = lista.copy()
    tamanho = len(lista_ordenada)
    passos = 0

    for i in range(tamanho):
        passos += 2  # controle do loop externo + atribuição inicial do menor índice
        indice_menor = i

        for j in range(i + 1, tamanho):
            passos += 2  # controle do loop interno + comparação de elementos

            if lista_ordenada[j] < lista_ordenada[indice_menor]:
                indice_menor = j
                passos += 1  # atualização do índice do menor elemento

        passos += 1  # verificação do if indice_menor != i
        
        if indice_menor != i:
            lista_ordenada[i], lista_ordenada[indice_menor] = (
                lista_ordenada[indice_menor],
                lista_ordenada[i],
            )
            passos += 3  # troca final de posição (duas atribuições + operação de swap)

    return lista_ordenada, passos


def insertion_sort(lista: List[str]) -> Tuple[List[str], int]:
    """Ordena uma lista utilizando Insertion Sort e contabiliza os passos

    Args:
        lista (List[str]): Lista a ser ordenada

    Returns:
        Tuple[List[str], int]: 
            - Lista ordenada 
            - Quantidade de passos executados
    """
    
    lista_ordenada = lista.copy()
    passos = 0

    for i in range(1, len(lista_ordenada)):
        passos += 3  # controle do loop externo + atribuição da chave + inicialização da variável j
        chave = lista_ordenada[i]
        j = i - 1
        
        passos += 1  # primeira verificação do while
        
        while j >= 0 and lista_ordenada[j] > chave:
            passos += 4  # verificação das duas condições do while + deslocamento do elemento para a direita + decremento de j
            lista_ordenada[j + 1] = lista_ordenada[j]
            j -= 1
            passos += 1  # nova verificação do while

        lista_ordenada[j + 1] = chave
        passos += 1  # inserção da chave na posição correta

    return lista_ordenada, passos


def medir_desempenho(
    funcao_ordenacao: Callable[[List[str]], Tuple[List[str], int]],
    lista: List[str],
) -> Tuple[float, int]:
    """Mede tempo de execução e passos de um algoritmo

    Args:
        funcao_ordenacao (Callable): Função de ordenação
        lista (List[str]): Lista a ser ordenada

    Returns:
        Tuple[float, int]: 
            - Tempo em segundos
            - Quantidade de passos.
    """
    
    inicio = time.perf_counter()
    _, passos = funcao_ordenacao(lista)
    fim = time.perf_counter()

    tempo_execucao = fim - inicio
    return tempo_execucao, passos


def gerar_lista_teste(tamanho: int, tipo: str) -> List[int]:
    """Gera listas de teste para demonstração

    Args:
        tamanho (int): Quantidade de elementos
        tipo (str): Tipo da lista (ordenada, aleatoria, inversa)

    Returns:
        List[int]: Lista gerada
    """
    
    lista = list(range(tamanho))

    if tipo == "ordenada":
        return lista
    elif tipo == "inversa":
        return lista[::-1]
    elif tipo == "aleatoria":
        random.shuffle(lista)
        return lista

    return lista


def demonstrar_algoritmos() -> None:
    """Executa os algoritmos com listas menores para demonstrar funcionamento e crescimento de tempo e passos
    """
    
    tamanhos = [10, 50, 100, 500, 1000, 10000]
    tipos = ["ordenada", "aleatoria", "inversa"]

    algoritmos: Dict[str, Callable] = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
    }

    print("=== Demostração dos Algoritmos de Ordenação ===")

    for tamanho in tamanhos:
        print(f"\nTamanho da lista: {tamanho}")

        for tipo in tipos:
            print(f"\n=> Lista {tipo.capitalize()}:")

            lista = gerar_lista_teste(tamanho, tipo)

            for nome, funcao in algoritmos.items():
                tempo, passos = medir_desempenho(funcao, lista)
                print(
                    f"{nome:<15} | Tempo: {tempo:.6f}s | Passos: {passos}"
                )
               
        print() 
        print("=" * 30)


def comparar_algoritmos(caminho_arquivo: str) -> None:
    """Executa os três algoritmos e exibe comparação final com porcentagens

    Args:
        caminho_arquivo (str): Caminho do arquivo com a listagem
    """
    
    lista = ler_listagem_arquivos(caminho_arquivo)

    algoritmos: Dict[str, Callable] = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
    }

    resultados = {}

    print("\n=== Comparação dos Algoritmos com Listagem de Arquivos ===")
    print(f"\nQuantidade de arquivos analisados: {len(lista)}\n")

    for nome, funcao in algoritmos.items():
        print(f"Executando {nome}...")
        tempo, passos = medir_desempenho(funcao, lista)
        resultados[nome] = {"tempo": tempo, "passos": passos}
        print(f"Tempo: {tempo:.6f} segundos")
        print(f"Passos: {passos}\n")

    print("=== Comparação Final ===")

    melhor_tempo = min(resultados.values(), key=lambda x: x["tempo"])["tempo"]
    menor_passos = min(resultados.values(), key=lambda x: x["passos"])["passos"]

    for nome, dados in resultados.items():
        diferenca_tempo = (
            (dados["tempo"] - melhor_tempo) / melhor_tempo * 100
        )
        diferenca_passos = (
            (dados["passos"] - menor_passos) / menor_passos * 100
        )

        print(
            f"{nome:<15} | "
            f"Tempo: {dados['tempo']:.6f}s "
            f"({diferenca_tempo:+.2f}%) | "
            f"Passos: {dados['passos']} "
            f"({diferenca_passos:+.2f}%)"
        )

demonstrar_algoritmos()
caminho_arquivo = "lista_arquivos.txt"
comparar_algoritmos(caminho_arquivo)
