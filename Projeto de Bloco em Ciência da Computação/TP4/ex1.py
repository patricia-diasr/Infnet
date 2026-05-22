import time
from typing import List, Optional, Tuple


class Processo:
    """
    Representa um processo no simulador de sistema operacional

    Attributes:
        pid (int): Identificador único do processo
        nome (str): Nome descritivo do processo
        burst_total (int): Tempo total de CPU necessário para concluir o processo
        burst_restante (int): Tempo de CPU ainda pendente de execução
        prioridade (int): Prioridade do processo baseada no burst total
        estado (str): Estado atual do processo
        tempo_espera (int): Tempo total gasto nas filas
        tempo_retorno (int): Tempo total desde a criação até o término
        ciclos_cpu (int): Número de vezes que o processo ocupou a CPU
        evento_pendente (Optional[int]): Quantidade de ciclos que o processo ficara suspenso
    """

    def __init__(self, pid: int, nome: str, burst_total: int, evento_pendente: Optional[int] = None) -> None:
        self.pid: int = pid
        self.nome: str = nome
        self.burst_total: int = burst_total
        self.burst_restante: int = burst_total
        self.prioridade: int = burst_total
        self.estado: str = "Nova"
        self.tempo_espera: int = 0
        self.tempo_retorno: int = 0
        self.ciclos_cpu: int = 0
        self.evento_pendente: Optional[int] = evento_pendente


    def __lt__(self, outro: "Processo") -> bool:
        return self.prioridade < outro.prioridade


    def __repr__(self) -> str:
        return f"Processo(pid = {self.pid}, nome = {self.nome!r}, burst_restante = {self.burst_restante}, estado = {self.estado!r})"


class HeapMinima:
    """
    Heap mínima baseada em prioridade numérica

    Attributes:
        _dados (List): Lista interna que armazena os elementos da heap
        _tamanho (int): Número de elementos atualmente na heap
    """

    def __init__(self) -> None:
        self._dados: List = []
        self._tamanho: int = 0


    def inserir(self, elemento) -> None:
        """
        Insere um novo elemento na heap mantendo a propriedade de heap mínima

        Args:
            elemento: Elemento a ser inserido, deve suportar comparação com menor que
        """

        self._dados.append(elemento)
        self._tamanho += 1
        self._subir(self._tamanho - 1)


    def extrair_minimo(self):
        """
        Remove e retorna o elemento de menor prioridade da heap

        Returns:
            Elemento de menor valor na heap

        Raises:
            IndexError: Se a heap estiver vazia
        """

        if self._tamanho == 0:
            raise IndexError("Heap mínima vazia")

        minimo = self._dados[0]
        self._tamanho -= 1

        if self._tamanho > 0:
            self._dados[0] = self._dados.pop()
            self._descer(0)

        else:
            self._dados.pop()

        return minimo


    def espiar_minimo(self):
        """
        Retorna o elemento de menor prioridade sem removê-lo

        Returns:
            Elemento de menor valor na heap

        Raises:
            IndexError: Se a heap estiver vazia
        """

        if self._tamanho == 0:
            raise IndexError("Heap mínima vazia")

        return self._dados[0]


    def esta_vazia(self) -> bool:
        """
        Verifica se a heap esta vazia

        Returns:
            bool: True se a heap não contém elementos
        """

        return self._tamanho == 0


    def tamanho(self) -> int:
        """
        Retorna o número de elementos na heap

        Returns:
            int: Quantidade de elementos
        """

        return self._tamanho


    def listar(self) -> List:
        """
        Retorna uma copia da lista interna da heap sem garantia de ordem

        Returns:
            List: Copia dos elementos internos
        """

        return list(self._dados[:self._tamanho])


    def _pai(self, i: int) -> int:
        """
        Retorna o índice do nó pai de um elemento

        Args:
            i (int): Índice do elemento filho

        Returns:
            int: Índice do pai
        """

        return (i - 1) // 2


    def _filho_esquerdo(self, i: int) -> int:
        """
        Retorna o índice do filho esquerdo de um elemento

        Args:
            i (int): Índice do elemento pai

        Returns:
            int: Índice do filho esquerdo
        """

        return 2 * i + 1


    def _filho_direito(self, i: int) -> int:
        """
        Retorna o índice do filho direito de um elemento

        Args:
            i (int): Índice do elemento pai

        Returns:
            int: Índice do filho direito
        """

        return 2 * i + 2


    def _trocar(self, i: int, j: int) -> None:
        """
        Troca dois elementos de posição na heap

        Args:
            i (int): Índice do primeiro elemento
            j (int): Índice do segundo elemento
        """

        self._dados[i], self._dados[j] = self._dados[j], self._dados[i]


    def _subir(self, i: int) -> None:
        """
        Sobe um elemento recém inserido até sua posicao correta na heap

        Args:
            i (int): Índice do elemento a ser subido
        """

        while i > 0 and self._dados[self._pai(i)] > self._dados[i]:
            self._trocar(i, self._pai(i))
            i = self._pai(i)


    def _descer(self, i: int) -> None:
        """
        Desce um elemento até sua posição correta após remoção da raiz

        Args:
            i (int): Índice do elemento a ser descido
        """

        menor = i
        esq = self._filho_esquerdo(i)
        dir = self._filho_direito(i)

        if esq < self._tamanho and self._dados[esq] < self._dados[menor]:
            menor = esq

        if dir < self._tamanho and self._dados[dir] < self._dados[menor]:
            menor = dir

        if menor != i:
            self._trocar(i, menor)
            self._descer(menor)


    def __repr__(self) -> str:
        return f"HeapMinima(tamanho = {self._tamanho})"


class SimuladorSO:
    """
    Simulador do ciclo de vida de processos em um sistema operacional com escalonamento por prioridade

    Attributes:
        quantum (int): Tempo máximo que um processo pode ocupar a CPU continuamente
        fila_pronta (HeapMinima): Heap mínima com processos prontos para execução
        fila_suspensa (HeapMinima): Heap mínima com processos aguardando eventos externos
        executando (Optional[Processo]): Processo atualmente em execução na CPU
        terminados (List[Processo]): Lista de processos que concluíram a execução
        relogio (int): Contador global de ciclos de simulação
        historico (List[dict]): Registro de cada ciclo para exibição da tabela final
    """

    def __init__(self, quantum: int) -> None:
        self.quantum: int = quantum
        self.fila_pronta: HeapMinima = HeapMinima()
        self.fila_suspensa: HeapMinima = HeapMinima()
        self.executando: Optional[Processo] = None
        self.terminados: List[Processo] = []
        self.relogio: int = 0
        self.historico: List[dict] = []


    def admitir(self, processo: Processo) -> None:
        """
        Admite um processo novo no simulador carregando-o para a fila de prontos

        Args:
            processo (Processo): Processo no estado Nova a ser admitido
        """

        processo.estado = "Pronta"
        self.fila_pronta.inserir(processo)


    def executar(self, processos: List[Processo]) -> None:
        """
        Executa a simulação completa para uma lista de processos

        Args:
            processos (List[Processo]): Lista de processos a serem simulados
        """

        print(f"\n{'=' * 60}")
        print(f"Simulador de Processos  |  Quantum: {self.quantum}  |  Processos: {len(processos)}")
        print(f"{'=' * 60}\n")

        for processo in processos:
            self.admitir(processo)
            self._snapshot(f"P{processo.pid} admitido (Nova -> Pronta)")

        total = len(processos)

        while len(self.terminados) < total:
            self._executar_ciclo()

        print("Simulacao concluida\n")


    def exibir_tabela_ciclos(self) -> None:
        """
        Exibe o histórico de ciclos em formato tabular com os estados de cada estrutura
        """

        col_ciclo = 10
        col_evento = 42
        col_cpu = 8
        col_prontos = 35
        col_suspensos = 14
        col_term = 35

        separador = (f"+{'-' * (col_ciclo + 2)}+{'-' * (col_evento + 2)}+{'-' * (col_cpu + 2)}+{'-' * (col_prontos + 2)}+{'-' * (col_suspensos + 2)}+{'-' * (col_term + 2)}+")

        cabecalho = (
            f"| {'Ciclo':^{col_ciclo}} "
            f"| {'Evento':^{col_evento}} "
            f"| {'CPU':^{col_cpu}} "
            f"| {'Fila Pronta':^{col_prontos}} "
            f"| {'Fila Suspensa':^{col_suspensos}} "
            f"| {'Terminados':^{col_term}} |"
        )

        print("\n============= Tabela de Ciclos de Simulação =============\n")
        print(separador)
        print(cabecalho)
        print(separador)

        for entrada in self.historico:
            ciclo = str(entrada["ciclo"])
            evento = entrada["evento"]
            cpu = str(entrada["cpu"]) if entrada["cpu"] is not None else "-"
            prontos = str(entrada["prontos"]) if entrada["prontos"] else "[]"
            suspensos = str(entrada["suspensos"]) if entrada["suspensos"] else "[]"
            term = str(entrada["terminados"]) if entrada["terminados"] else "[]"

            print(
                f"| {ciclo:^{col_ciclo}} "
                f"| {evento:<{col_evento}} "
                f"| {cpu:^{col_cpu}} "
                f"| {prontos:<{col_prontos}} "
                f"| {suspensos:<{col_suspensos}} "
                f"| {term:<{col_term}} |"
            )

        print(separador)


    def exibir_tabela_processos(self) -> None:
        """
        Exibe uma tabela com o resumo estatístico de cada processo após o término da simulacao
        """

        col_pid = 5
        col_nome = 25
        col_burst = 8
        col_ciclos = 8
        col_espera = 8
        col_retorno = 9

        separador = (f"+{'-' * (col_pid + 2)}+{'-' * (col_nome + 2)}+{'-' * (col_burst + 2)}+{'-' * (col_ciclos + 2)}+{'-' * (col_espera + 2)}+{'-' * (col_retorno + 2)}+")

        cabecalho = (
            f"| {'PID':^{col_pid}} "
            f"| {'Nome':^{col_nome}} "
            f"| {'Burst':^{col_burst}} "
            f"| {'Ciclos':^{col_ciclos}} "
            f"| {'Espera':^{col_espera}} "
            f"| {'Retorno':^{col_retorno}} |"
        )

        print("\n\n============= Resumo por Processo =============\n")
        print(separador)
        print(cabecalho)
        print(separador)

        for processo in sorted(self.terminados, key=lambda p: p.pid):
            print(
                f"| {str(processo.pid):^{col_pid}} "
                f"| {processo.nome:<{col_nome}} "
                f"| {str(processo.burst_total):^{col_burst}} "
                f"| {str(processo.ciclos_cpu):^{col_ciclos}} "
                f"| {str(processo.tempo_espera):^{col_espera}} "
                f"| {str(processo.tempo_retorno):^{col_retorno}} |"
            )

        print(separador)
        print()


    def _snapshot(self, evento: str) -> None:
        """
        Registra o estado atual de todas as estruturas no historico do simulador

        Args:
            evento (str): Descrição do evento que provocou a mudança de estado
        """

        prontos = [p.pid for p in sorted(self.fila_pronta.listar(), key=lambda p: p.prioridade)]
        suspensos = [p.pid for p in sorted(self.fila_suspensa.listar(), key=lambda p: p.prioridade)]
        em_cpu = self.executando.pid if self.executando else None
        terminados_ids = [p.pid for p in self.terminados]

        self.historico.append({
            "ciclo": self.relogio,
            "evento": evento,
            "cpu": em_cpu,
            "prontos": prontos,
            "suspensos": suspensos,
            "terminados": terminados_ids
        })


    def _processar_suspensos(self) -> None:
        """
        Decrementa o contador de espera de cada processo suspenso e move para pronta os que concluíram
        """

        remanescentes: List[Processo] = []

        while not self.fila_suspensa.esta_vazia():
            remanescentes.append(self.fila_suspensa.extrair_minimo())

        for processo in remanescentes:
            processo.evento_pendente -= 1

            if processo.evento_pendente <= 0:
                processo.evento_pendente = None
                processo.estado = "Pronta"
                self.fila_pronta.inserir(processo)

            else:
                self.fila_suspensa.inserir(processo)


    def _executar_ciclo(self) -> None:
        """
        Executa um ciclo completo de escalonamento: processa suspensos, escalona, executa e transicionamento
        """

        self._processar_suspensos()

        if self.executando is None and not self.fila_pronta.esta_vazia():
            self.executando = self.fila_pronta.extrair_minimo()
            self.executando.estado = "Executando"
            self.executando.ciclos_cpu += 1
            self._snapshot(f"P{self.executando.pid} escalado para CPU")

        if self.executando is None:
            self._snapshot("CPU ociosa")
            return

        tempo_execucao = min(self.quantum, self.executando.burst_restante)
        self.executando.burst_restante -= tempo_execucao
        time.sleep(tempo_execucao * TEMPO_EXECUCAO_REAL)

        if self.executando.burst_restante == 0:
            self.executando.estado = "Terminada"
            self.executando.tempo_retorno = self.relogio + tempo_execucao
            self.terminados.append(self.executando)
            self._snapshot(f"P{self.executando.pid} concluído apos {tempo_execucao} unidade(s)")
            self.executando = None

        elif self.executando.evento_pendente is not None:
            self.executando.estado = "Suspensa"
            self._snapshot(f"P{self.executando.pid} suspenso aguardando evento")
            self.fila_suspensa.inserir(self.executando)
            self.executando = None

        else:
            self._snapshot(f"P{self.executando.pid} preemptado por fim de quantum")
            self.executando.estado = "Pronta"
            self.fila_pronta.inserir(self.executando)
            self.executando = None

        self.relogio += 1

        for processo in self.fila_pronta.listar():
            processo.tempo_espera += 1


QUANTUM = 3
TEMPO_EXECUCAO_REAL = 0.3

processos_simulacao: List[Processo] = [
    Processo(pid=1, nome="Navegador", burst_total=12),
    Processo(pid=2, nome="Editor de texto", burst_total=9),
    Processo(pid=3, nome="Compilador", burst_total=15),
    Processo(pid=4, nome="Player de áudio", burst_total=6),
    Processo(pid=5, nome="Antivírus", burst_total=18, evento_pendente=2),
    Processo(pid=6, nome="Gerenciador de arquivos", burst_total=7),
    Processo(pid=7, nome="Atualizador", burst_total=21, evento_pendente=3),
    Processo(pid=8, nome="Terminal", burst_total=10),
    Processo(pid=9, nome="Indexador", burst_total=14, evento_pendente=1),
    Processo(pid=10, nome="Backup", burst_total=24),
]

simulador = SimuladorSO(quantum=QUANTUM)
simulador.executar(processos_simulacao)
simulador.exibir_tabela_ciclos()
simulador.exibir_tabela_processos()
