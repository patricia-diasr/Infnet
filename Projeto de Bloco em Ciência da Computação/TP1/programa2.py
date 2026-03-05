import time
import random
import tracemalloc
from typing import List, Tuple, Dict, Callable
from collections import deque


class TabelaHash:
    """Implementação de uma tabela hash"""

    def __init__(self):
        """Inicializa a tabela hash"""
        self.tabela: Dict[int, str] = {}
        self.passos = 0

    def inserir(self, chave: int, valor: str) -> None:
        """Insere um elemento na tabela hash"""
        self.tabela[chave] = valor
        self.passos += 1  # atribuição na tabela

    def buscar(self, chave: int) -> str:
        """Busca um elemento na tabela hash"""
        self.passos += 1  # acesso à estrutura
        return self.tabela.get(chave)

    def remover(self, chave: int) -> None:
        """Remove um elemento da tabela hash"""
        if chave in self.tabela:
            del self.tabela[chave]
            self.passos += 1  # remoção da estrutura

    def tamanho(self) -> int:
        """Retorna o tamanho da tabela"""
        return len(self.tabela)


class Pilha:
    """Implementação de uma pilha"""

    def __init__(self):
        """Inicializa a pilha"""
        self.itens: List[str] = []
        self.passos = 0  # controle de passos

    def empilhar(self, item: str) -> None:
        """Adiciona item ao topo da pilha"""
        self.itens.append(item)
        self.passos += 1  # inserção na lista

    def desempilhar(self) -> str:
        """Remove item do topo da pilha"""
        if self.itens:
            self.passos += 1  # remoção da lista
            return self.itens.pop()

    def buscar_posicao(self, posicao: int) -> str:
        """Busca elemento por posição"""
        if 0 <= posicao < len(self.itens):
            self.passos += 1  # acesso à lista
            return self.itens[posicao]

    def tamanho(self) -> int:
        """Retorna o tamanho da pilha"""
        return len(self.itens)


class Fila:
    """Implementação de uma fila"""

    def __init__(self):
        """Inicializa a fila"""
        self.itens = deque()
        self.passos = 0  # controle de passos

    def enfileirar(self, item: str) -> None:
        """Adiciona item ao final da fila"""
        self.itens.append(item)
        self.passos += 1  # inserção na estrutura

    def desenfileirar(self) -> str:
        """Remove item do início da fila"""
        if self.itens:
            self.passos += 1  # remoção da estrutura
            return self.itens.popleft()

    def buscar_posicao(self, posicao: int) -> str:
        """Busca elemento por posição"""
        if 0 <= posicao < len(self.itens):
            self.passos += 1  # acesso à estrutura
            return list(self.itens)[posicao]

    def tamanho(self) -> int:
        """Retorna o tamanho da fila"""
        return len(self.itens)


def ler_listagem_arquivos(caminho_arquivo: str) -> List[str]:
    """Lê um arquivo de texto contendo a listagem de arquivos

    Args:
        caminho_arquivo (str): Caminho para o arquivo de texto

    Returns:
        List[str]: Lista contendo os nomes dos arquivos
    """

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]


def medir_tempo_memoria(funcao: Callable) -> Tuple[float, float]:
    """Mede tempo e memória de execução

    Args:
        funcao (Callable): Função a ser executada

    Returns:
        Tuple[float, float]:
            - Tempo em segundos
            - Memória em KB
    """

    tracemalloc.start()
    inicio = time.perf_counter()

    funcao()

    fim = time.perf_counter()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tempo_execucao = fim - inicio
    memoria_kb = memoria_pico / 1024

    return tempo_execucao, memoria_kb


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


def executar_tabela_hash(lista: List[str]) -> Dict[str, Dict]:
    """Executa operações de inserção, busca e remoção na Tabela Hash realizando a mensuração de tempo e memória 
    para cada operação

    Args:
        lista (List[str]): Lista base contendo os elementos a serem inseridos

    Returns:
        Dict[str, Dict]:
            - Inserção: tempo e memória
            - Busca: tempo e memória
            - Remoção: tempo e memória
            - Quantidade total de passos executados
    """

    tabela = TabelaHash()

    def inserir():
        for i, item in enumerate(lista):
            tabela.inserir(i, item)

    def buscar():
        for pos in [1, 100, 1000, 5000, len(lista) - 1]:
            if pos < len(lista):
                tabela.buscar(pos)

    def remover():
        tabela.remover(1)

    tempo_ins, mem_ins = medir_tempo_memoria(inserir)
    tempo_bus, mem_bus = medir_tempo_memoria(buscar)
    tempo_rem, mem_rem = medir_tempo_memoria(remover)

    return {
        "insercao": {"tempo": tempo_ins, "memoria": mem_ins},
        "busca": {"tempo": tempo_bus, "memoria": mem_bus},
        "remocao": {"tempo": tempo_rem, "memoria": mem_rem},
        "passos": tabela.passos,
    }


def executar_pilha(lista: List[str]) -> Dict[str, Dict]:
    """Executa operações de empilhamento, busca por posição e desempilhamento na Pilha realizando a mensuração de tempo e memória 
    para cada operação

    Args:
        lista (List[str]): Lista base contendo os elementos a serem inseridos

    Returns:
        Dict[str, Dict]:
            - Inserção: tempo e memória
            - Busca: tempo e memória
            - Remoção: tempo e memória
            - Quantidade total de passos executados
    """

    pilha = Pilha()

    def inserir():
        for item in lista:
            pilha.empilhar(item)

    def buscar():
        for pos in [1, 100, 1000, 5000, len(lista) - 1]:
            if pos < len(lista):
                pilha.buscar_posicao(pos)

    def remover():
        pilha.desempilhar()

    tempo_ins, mem_ins = medir_tempo_memoria(inserir)
    tempo_bus, mem_bus = medir_tempo_memoria(buscar)
    tempo_rem, mem_rem = medir_tempo_memoria(remover)

    return {
        "insercao": {"tempo": tempo_ins, "memoria": mem_ins},
        "busca": {"tempo": tempo_bus, "memoria": mem_bus},
        "remocao": {"tempo": tempo_rem, "memoria": mem_rem},
        "passos": pilha.passos,
    }


def executar_fila(lista: List[str]) -> Dict[str, Dict]:
    """Executa operações de enfileiramento, busca por posição e desenfileiramento na Fila realizando a mensuração de tempo e 
    memória para cada operação

    Args:
        lista (List[str]): Lista base contendo os elementos a serem inseridos

    Returns:
        Dict[str, Dict]:
            - Inserção: tempo e memória
            - Busca: tempo e memória
            - Remoção: tempo e memória
            - Quantidade total de passos executados
    """

    fila = Fila()

    def inserir():
        for item in lista:
            fila.enfileirar(item)

    def buscar():
        for pos in [1, 100, 1000, 5000, len(lista) - 1]:
            if pos < len(lista):
                fila.buscar_posicao(pos)

    def remover():
        fila.desenfileirar()

    tempo_ins, mem_ins = medir_tempo_memoria(inserir)
    tempo_bus, mem_bus = medir_tempo_memoria(buscar)
    tempo_rem, mem_rem = medir_tempo_memoria(remover)

    return {
        "insercao": {"tempo": tempo_ins, "memoria": mem_ins},
        "busca": {"tempo": tempo_bus, "memoria": mem_bus},
        "remocao": {"tempo": tempo_rem, "memoria": mem_rem},
        "passos": fila.passos,
    }


def executar_testes_estruturas(lista: List[str]) -> Dict[str, Dict]:
    """Executa as três estruturas de dados (Tabela Hash, Pilha e Fila) realizando inserção, busca e remoção de elementos com 
    mensuração de tempo e memória

    Args:
        lista (List[str]): Lista base contendo os dados a serem processados

    Returns:
        Dict[str, Dict]:
            Dicionário contendo, para cada estrutura:
                - Inserção: tempo e memória
                - Busca: tempo e memória
                - Remoção: tempo e memória
                - Quantidade total de passos executados
    """

    return {
        "Tabela Hash": executar_tabela_hash(lista),
        "Pilha": executar_pilha(lista),
        "Fila": executar_fila(lista),
    }
    

def demonstrar_estruturas() -> None:
    """Executa as estruturas com listas menores para demonstrar funcionamento,
    crescimento de tempo, memória e passos
    """

    tamanhos = [10, 50, 100, 500, 1000, 10000]
    tipos = ["ordenada", "aleatoria", "inversa"]

    print("=== Demonstração das Estruturas de Dados ===")

    for tamanho in tamanhos:
        print(f"\nTamanho da lista: {tamanho}")

        for tipo in tipos:
            print(f"\n=> Lista {tipo.capitalize()}:")

            lista = gerar_lista_teste(tamanho, tipo)
            resultados = executar_testes_estruturas(lista)

            for nome, dados in resultados.items():

                tempo_total = (
                    dados["insercao"]["tempo"]
                    + dados["busca"]["tempo"]
                    + dados["remocao"]["tempo"]
                )

                memoria_total = max(
                    dados["insercao"]["memoria"],
                    dados["busca"]["memoria"],
                    dados["remocao"]["memoria"],
                )

                print(f"\n{nome}:")
                print(
                    f"  Inserção  -> Tempo: {dados['insercao']['tempo']:.6f}s | "
                    f"Memória: {dados['insercao']['memoria']:.2f} KB"
                )
                print(
                    f"  Busca     -> Tempo: {dados['busca']['tempo']:.6f}s | "
                    f"Memória: {dados['busca']['memoria']:.2f} KB"
                )
                print(
                    f"  Remoção   -> Tempo: {dados['remocao']['tempo']:.6f}s | "
                    f"Memória: {dados['remocao']['memoria']:.2f} KB"
                )

                print(
                    f"  Total     -> Tempo: {tempo_total:.6f}s | "
                    f"Memória: {memoria_total:.2f} KB | "
                    f"Passos: {dados['passos']}"
                )

        print("\n" + "=" * 50)
        
        
def comparar_estruturas(caminho_arquivo: str) -> None:
    """Executa as estruturas com a listagem real e exibe comparação percentual final

    Args:
        caminho_arquivo (str): Caminho do arquivo com a listagem
    """

    lista = ler_listagem_arquivos(caminho_arquivo)

    print("\n=== Comparação das Estruturas com Listagem de Arquivos ===")
    print(f"\nQuantidade de arquivos analisados: {len(lista)}\n")

    resultados = executar_testes_estruturas(lista)
    resultados_finais = {}

    for nome, dados in resultados.items():

        tempo_total = (
            dados["insercao"]["tempo"]
            + dados["busca"]["tempo"]
            + dados["remocao"]["tempo"]
        )

        memoria_total = max(
            dados["insercao"]["memoria"],
            dados["busca"]["memoria"],
            dados["remocao"]["memoria"],
        )

        resultados_finais[nome] = {
            "tempo": tempo_total,
            "memoria": memoria_total,
            "passos": dados["passos"],
        }

        print(f"{nome}:")
        print(
            f"  Inserção  -> Tempo: {dados['insercao']['tempo']:.6f}s | "
            f"Memória: {dados['insercao']['memoria']:.2f} KB"
        )
        print(
            f"  Busca     -> Tempo: {dados['busca']['tempo']:.6f}s | "
            f"Memória: {dados['busca']['memoria']:.2f} KB"
        )
        print(
            f"  Remoção   -> Tempo: {dados['remocao']['tempo']:.6f}s | "
            f"Memória: {dados['remocao']['memoria']:.2f} KB"
        )
        print(
            f"  Total     -> Tempo: {tempo_total:.6f}s | "
            f"Memória: {memoria_total:.2f} KB | "
            f"Passos: {dados['passos']}\n"
        )

    print("=== Comparação Final (Tempo Total) ===")

    melhor_tempo = min(resultados_finais.values(), key=lambda x: x["tempo"])["tempo"]
    menor_memoria = min(resultados_finais.values(), key=lambda x: x["memoria"])["memoria"]
    menor_passos = min(resultados_finais.values(), key=lambda x: x["passos"])["passos"]

    for nome, dados in resultados_finais.items():

        diferenca_tempo = (
            (dados["tempo"] - melhor_tempo) / melhor_tempo * 100
            if melhor_tempo > 0 else 0
        )

        diferenca_memoria = (
            (dados["memoria"] - menor_memoria) / menor_memoria * 100
            if menor_memoria > 0 else 0
        )

        diferenca_passos = (
            (dados["passos"] - menor_passos) / menor_passos * 100
            if menor_passos > 0 else 0
        )

        print(
            f"{nome:<15} | "
            f"Tempo Total: {dados['tempo']:.6f}s ({diferenca_tempo:+.2f}%) | "
            f"Memória: {dados['memoria']:.2f} KB ({diferenca_memoria:+.2f}%) | "
            f"Passos: {dados['passos']} ({diferenca_passos:+.2f}%)"
        )
        
    
demonstrar_estruturas()
caminho_arquivo = "lista_arquivos.txt"
comparar_estruturas(caminho_arquivo)
