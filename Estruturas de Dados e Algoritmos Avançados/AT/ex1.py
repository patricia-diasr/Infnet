from typing import Optional
import time
import random


class AgendadorErroFilaVazia(Exception):
    """Levantada ao tentar executar uma tarefa em um agendador sem tarefas pendentes"""


class ItemHeap:
    """
    Entrada interna da heap que associa uma tarefa à sua prioridade de avaliação

    Attributes:
        prioridade (int): Tempo virtual de conclusão usado como chave de ordenação
        id_tarefa (str): Identificador único da tarefa
        tempo (int): Tempo de execução da tarefa
        tecnologia (str): Grupo tecnológico ao qual a tarefa pertence
        removido (bool): Marca lógica usada pela lazy evaluation para invalidar entradas obsoletas
    """

    def __init__(self, prioridade: int, id_tarefa: str, tempo: int, tecnologia: str) -> None:
        self.prioridade: int = prioridade
        self.id_tarefa: str = id_tarefa
        self.tempo: int = tempo
        self.tecnologia: str = tecnologia
        self.removido: bool = False


    def __repr__(self) -> str:
        return (f"ItemHeap(id = {self.id_tarefa!r}, prioridade = {self.prioridade}, tecnologia = {self.tecnologia!r}, removido = {self.removido})")


class HeapMinima:
    """
    Heap mínima genérica baseada em vetor, ordenada pelo atributo prioridade dos itens

    Attributes:
        _dados (list): Vetor interno que armazena os itens da heap
        _tamanho (int): Número de itens válidos atualmente na heap
    """

    def __init__(self) -> None:
        self._dados: list = []
        self._tamanho: int = 0


    def _pai(self, i: int) -> int:
        return (i - 1) // 2


    def _filho_esq(self, i: int) -> int:
        return 2 * i + 1


    def _filho_dir(self, i: int) -> int:
        return 2 * i + 2


    def _trocar(self, i: int, j: int) -> None:
        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]


    def _subir(self, i: int) -> None:
        """
        Restaura a propriedade de heap subindo o elemento na posição i até sua posição correta

        Args:
            i (int): Índice do elemento a ser subido
        """

        while i > 0:
            pai = self._pai(i)

            if self._dados[i].prioridade < self._dados[pai].prioridade:
                self._trocar(i, pai)
                i = pai

            else:
                break


    def _descer(self, i: int) -> None:
        """
        Restaura a propriedade de heap descendo o elemento na posição i até sua posição correta

        Args:
            i (int): Índice do elemento a ser descido
        """

        while True:
            menor = i
            esq = self._filho_esq(i)
            dir = self._filho_dir(i)

            if esq < self._tamanho and self._dados[esq].prioridade < self._dados[menor].prioridade:
                menor = esq

            if dir < self._tamanho and self._dados[dir].prioridade < self._dados[menor].prioridade:
                menor = dir

            if menor != i:
                self._trocar(i, menor)
                i = menor

            else:
                break


    def inserir(self, item: ItemHeap) -> None:
        """
        Insere um item na heap mantendo a propriedade de heap mínima

        Args:
            item (ItemHeap): Item a ser inserido
        """

        if self._tamanho < len(self._dados):
            self._dados[self._tamanho] = item

        else:
            self._dados.append(item)

        self._tamanho += 1
        self._subir(self._tamanho - 1)


    def extrair_minimo(self) -> ItemHeap:
        """
        Remove e retorna o item com menor prioridade da heap

        Returns:
            ItemHeap: Item com menor prioridade

        Raises:
            AgendadorErroFilaVazia: Se a heap estiver vazia
        """

        if self._tamanho == 0:
            raise AgendadorErroFilaVazia("Nenhuma tarefa disponível para execução")

        self._trocar(0, self._tamanho - 1)
        self._tamanho -= 1
        item = self._dados[self._tamanho]

        if self._tamanho > 0:
            self._descer(0)

        return item


    def pico(self) -> Optional[ItemHeap]:
        """
        Retorna o item com menor prioridade sem removê-lo

        Returns:
            Optional[ItemHeap]: Item no topo da heap, ou None se vazia
        """

        return self._dados[0] if self._tamanho > 0 else None


    def tamanho(self) -> int:
        """
        Retorna o número de itens válidos na heap

        Returns:
            int: Quantidade de itens
        """

        return self._tamanho


    def __repr__(self) -> str:
        return f"HeapMinima(tamanho = {self._tamanho})"


class AgendadorOtimizado:
    """
    Agendador de tarefas que minimiza o tempo total de espera usando heap mínima com lazy evaluation

    Attributes:
        _heap (HeapMinima): Heap mínima interna que ordena as tarefas
        _tecnologia_atual (Optional[str]): Tecnologia da última tarefa executada
        _total_executadas (int): Contador de tarefas finalizadas
    """

    def __init__(self) -> None:
        self._heap: HeapMinima = HeapMinima()
        self._tecnologia_atual: Optional[str] = None
        self._total_executadas: int = 0


    def adicionar_tarefa(self, id_tarefa: str, tempo: int, tecnologia: str) -> None:
        """
        Insere uma nova tarefa no agendador com prioridade otimista sem penalidade

        Args:
            id_tarefa (str): Identificador único da tarefa
            tempo (int): Tempo de execução em unidades arbitrárias
            tecnologia (str): Grupo tecnológico da tarefa
        """

        item = ItemHeap(prioridade = tempo, id_tarefa = id_tarefa, tempo = tempo, tecnologia = tecnologia)
        self._heap.inserir(item)


    def executar_proxima(self, tecnologia_atual: str, penalidade: int) -> str:
        """
        Remove e retorna o identificador da melhor tarefa a executar no contexto atual

        Args:
            tecnologia_atual (str): Tecnologia em execução no momento da chamada
            penalidade (int): Custo de troca de contexto entre tecnologias distintas

        Returns:
            str: Identificador da tarefa selecionada para execução

        Raises:
            AgendadorErroFilaVazia: Se não houver tarefas disponíveis
        """

        if self._heap.tamanho() == 0:
            raise AgendadorErroFilaVazia("Nenhuma tarefa disponível para execução")

        while True:
            item = self._heap.extrair_minimo()

            if item.removido:
                continue

            mesma_tecnologia = item.tecnologia == tecnologia_atual
            prioridade_real = item.tempo if mesma_tecnologia else item.tempo + penalidade

            if item.prioridade >= prioridade_real:
                self._tecnologia_atual = item.tecnologia
                self._total_executadas += 1
                return item.id_tarefa

            item.prioridade = prioridade_real
            self._heap.inserir(item)


    def tamanho(self) -> int:
        """
        Retorna o número de tarefas ainda pendentes no agendador

        Returns:
            int: Quantidade de tarefas na fila
        """

        return self._heap.tamanho()


    def tecnologia_atual(self) -> Optional[str]:
        """
        Retorna a tecnologia da última tarefa executada

        Returns:
            Optional[str]: Nome da tecnologia, ou None se nenhuma tarefa foi executada
        """

        return self._tecnologia_atual


    def __repr__(self) -> str:
        return (f"AgendadorOtimizado(pendentes = {self.tamanho()}, executadas = {self._total_executadas}, tecnologia_atual = {self._tecnologia_atual!r})")


print("\n===== Teste 1 - Carga Inicial e Execução Sequencial =====\n")

tarefas_iniciais = [
    ("T1", 15, "Python"),
    ("T2", 8, "Java"),
    ("T3", 22, "Docker"),
    ("T4", 5, "Java"),
    ("T5", 12, "Python"),
    ("T7", 4, "C++"),
]

agendador = AgendadorOtimizado()

for id_tarefa, tempo, tecnologia in tarefas_iniciais:
    agendador.adicionar_tarefa(id_tarefa, tempo, tecnologia)

print(f"Tarefas carregadas: {agendador.tamanho()}")
print(f"Estado inicial: {agendador}\n")

PENALIDADE = 10
tecnologia_contexto = "Python"

print(f"Tecnologia inicial do servidor: '{tecnologia_contexto}'")
print(f"Penalidade de setup: {PENALIDADE}\n")
print(f"{'Ordem':<6}  {'Tarefa':>6}  {'Tecnologia Anterior':<22}  {'Tecnologia Atual':<18}")
print(f"{'-' * 6}  {'-' *6}  {'-' * 22}  {'-' * 18}")

ordem = 1

while agendador.tamanho() > 0:
    tecnologia_antes = tecnologia_contexto
    tarefa_id = agendador.executar_proxima(tecnologia_contexto, PENALIDADE)
    tecnologia_contexto = agendador.tecnologia_atual()
    print(f"{ordem:<6}  {tarefa_id:>6}  {tecnologia_antes:<22}  {tecnologia_contexto:<18}")
    ordem += 1

print(f"\nEstado final: {agendador}")


print("\n\n===== Teste 2 - Erro ao Executar com Fila Vazia =====\n")

agendador_vazio = AgendadorOtimizado()

try:
    agendador_vazio.executar_proxima("Python", 10)

except AgendadorErroFilaVazia as e:
    print(f"Exceção esperada: {e}")


print("\n\n===== Teste 3 - Penalidade Alta Favorece Agrupamento por Tecnologia =====\n")

tarefas_agrupamento = [
    ("A1", 10, "Python"),
    ("A2", 10, "Java"),
    ("A3", 10, "Python"),
    ("A4", 10, "Java"),
    ("A5", 10, "Python"),
    ("A6", 10, "Java"),
]

agendador_alto = AgendadorOtimizado()

for id_tarefa, tempo, tecnologia in tarefas_agrupamento:
    agendador_alto.adicionar_tarefa(id_tarefa, tempo, tecnologia)

PENALIDADE_ALTA = 50
tecnologia_contexto = "Python"
ordem_execucao = []

while agendador_alto.tamanho() > 0:
    tarefa_id = agendador_alto.executar_proxima(tecnologia_contexto, PENALIDADE_ALTA)
    tecnologia_contexto = agendador_alto.tecnologia_atual()
    ordem_execucao.append((tarefa_id, tecnologia_contexto))

print(f"Penalidade usada: {PENALIDADE_ALTA}")
print(f"Ordem esperada: agrupadas por tecnologia")
print(f"Ordem obtida: {[t for t, _ in ordem_execucao]}")
trocas = sum(
    1 for i in range(1, len(ordem_execucao))
    if ordem_execucao[i][1] != ordem_execucao[i - 1][1]
)
print(f"Trocas de tecnologia: {trocas} (ideal: 1)")


print("\n\n===== Teste 4 - Stress Test com 50.000 Tarefas =====\n")

tecnologias = ["Python", "Java", "Docker", "C++", "Go", "Rust"]
agendador_stress = AgendadorOtimizado()
random.seed(42)

for i in range(50_000):
    agendador_stress.adicionar_tarefa(id_tarefa = f"S{i}", tempo = random.randint(1, 1000), tecnologia = random.choice(tecnologias))

print(f"Tarefas inseridas: {agendador_stress.tamanho()}")

inicio = time.perf_counter()
tecnologia_contexto = "Python"
executadas = 0

while agendador_stress.tamanho() > 0:
    agendador_stress.executar_proxima(tecnologia_contexto, penalidade = 20)
    tecnologia_contexto = agendador_stress.tecnologia_atual()
    executadas += 1

fim = time.perf_counter()
duracao = fim - inicio

print(f"Tarefas executadas: {executadas}")
print(f"Tempo de execução: {duracao:.4f}s")
print(f"Resultado: {'APROVADO' if duracao < 0.5 else 'REPROVADO'} (limite: 0.5s)\n")
