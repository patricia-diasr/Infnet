import os
from typing import List, Optional, Tuple


class Linha:
    """
    Nó de uma lista duplamente encadeada que armazena uma linha de texto

    Attributes:
        texto (str): Conteúdo textual da linha
        anterior (Optional[Linha]): Ponteiro para a linha anterior na lista
        proximo (Optional[Linha]): Ponteiro para a próxima linha na lista
    """

    def __init__(self, texto: str) -> None:
        self.texto: str = texto
        self.anterior: Optional["Linha"] = None
        self.proximo: Optional["Linha"] = None


class EditorTexto:
    """
    Editor de texto baseado em lista duplamente encadeada com interface de comandos

    Attributes:
        primeira (Optional[Linha]): Aponta para a primeira linha do texto
        corrente (Optional[Linha]): Aponta para a linha atualmente selecionada
        total_linhas (int): Quantidade total de linhas no texto
    """

    def __init__(self) -> None:
        self.primeira: Optional[Linha] = None
        self.corrente: Optional[Linha] = None
        self.total_linhas: int = 0

    def _numero_corrente(self) -> int:
        """
        Retorna o número da linha corrente

        Returns:
            int: Posição da linha corrente, ou 0 se o editor estiver vazio
        """

        if self.corrente is None:
            return 0

        numero = 1
        atual = self.primeira

        while atual is not self.corrente:
            numero += 1
            atual = atual.proximo

        return numero

    def _obter_linha(self, numero: int) -> Optional[Linha]:
        """
        Retorna o nó correspondente ao número de linha

        Args:
            numero (int): Posição da linha desejada

        Returns:
            Optional[Linha]: Nó da linha ou None se o número for inválido
        """

        if numero < 1 or numero > self.total_linhas:
            return None

        atual = self.primeira

        for _ in range(numero - 1):
            atual = atual.proximo

        return atual

    def _inserir_depois_do_no(self, no: Optional[Linha], texto: str) -> Linha:
        """
        Insere uma nova linha imediatamente após o nó fornecido

        Args:
            no (Optional[Linha]): Nó após o qual a nova linha será inserida
            texto (str): Conteúdo da nova linha

        Returns:
            Linha: O nó criado
        """

        nova = Linha(texto)

        if no is None:
            nova.proximo = self.primeira

            if self.primeira is not None:
                self.primeira.anterior = nova
            
            self.primeira = nova

        else:
            proxima = no.proximo
            nova.anterior = no
            nova.proximo = proxima
            no.proximo = nova
            
            if proxima is not None:
                proxima.anterior = nova

        self.total_linhas += 1
        self.corrente = nova
        return nova

    def _remover_no(self, no: Linha) -> None:
        """
        Remove o nó fornecido da lista e reposiciona o ponteiro corrente

        Args:
            no (Linha): Nó a ser removido
        """

        anterior = no.anterior
        proxima = no.proximo

        if anterior is not None:
            anterior.proximo = proxima

        else:
            self.primeira = proxima

        if proxima is not None:
            proxima.anterior = anterior

        if self.corrente is no:
            self.corrente = anterior if anterior is not None else proxima

        self.total_linhas -= 1

    def cmd_inserir(self, n: Optional[int]) -> None:
        """
        Entra no modo de inserção, adicionando linhas digitadas após a linha n

        Args:
            n (Optional[int]): Número da linha após a qual inserir; None usa a corrente
        """

        if n is not None:
            ancora = self._obter_linha(n)
            
            if ancora is None and n != 0:
                print(f"  Erro: linha {n} não existe.")
                return
            
        else:
            ancora = self.corrente

        print("  (modo inserção — linha em branco para encerrar)")
        ultima_inserida = ancora

        while True:
            texto = input("  => ")
            
            if texto == "":
                break
        
            ultima_inserida = self._inserir_depois_do_no(ultima_inserida, texto)

    def cmd_excluir(self, i: Optional[int], f: Optional[int]) -> None:
        """
        Exclui as linhas de i até f

        Args:
            i (Optional[int]): Número da primeira linha a excluir
            f (Optional[int]): Número da última linha a excluir
        """

        if i is None:
            if self.corrente is None:
                print("  Erro: editor vazio.")
                return
            
            self._remover_no(self.corrente)
            print("  Linha corrente excluída.")
            return

        f = f if f is not None else i

        if i > f:
            print("  Erro: i deve ser menor ou igual a f.")
            return

        nos = [self._obter_linha(num) for num in range(i, f + 1)]

        if any(no is None for no in nos):
            print(f"  Erro: intervalo [{i}, {f}] contém linhas inválidas.")
            return

        for no in nos:
            self._remover_no(no)

        print(f"  {len(nos)} linha(s) excluída(s).")

    def cmd_duplicar(self, i: int, f: int, p: int) -> None:
        """
        Duplica o bloco de linhas i até f imediatamente após a linha p

        Args:
            i (int): Número da primeira linha do bloco a duplicar
            f (int): Número da última linha do bloco a duplicar
            p (int): Número da linha após a qual o bloco será inserido
        """

        if i > f:
            print("  Erro: i deve ser menor ou igual a f.")
            return

        ancora = self._obter_linha(p)

        if ancora is None and p != 0:
            print(f"  Erro: linha de destino {p} não existe.")
            return

        textos: List[str] = []
        
        for num in range(i, f + 1):
            no = self._obter_linha(num)
        
            if no is None:
                print(f"  Erro: linha {num} não existe.")
                return
        
            textos.append(no.texto)

        ultima = ancora
        
        for texto in textos:
            ultima = self._inserir_depois_do_no(ultima, texto)

        print(f"  {len(textos)} linha(s) duplicada(s) após a linha {p}.")

    def cmd_listar(self, i: Optional[int], f: Optional[int]) -> None:
        """
        Lista as linhas de i até f com seus respectivos números

        Args:
            i (Optional[int]): Número da primeira linha a listar
            f (Optional[int]): Número da última linha a listar, caso None, vai até o fim
        """

        if self.primeira is None:
            print("  (editor vazio)")
            return

        inicio = i if i is not None else 1
        fim = f if f is not None else self.total_linhas

        for num in range(inicio, fim + 1):
            no = self._obter_linha(num)
   
            if no is None:
                print(f"  Erro: linha {num} não existe.")
                return
   
            marcador = " ←" if no is self.corrente else "  "
            print(f"  {num:>4}{marcador}  {no.texto}")

    def cmd_carregar(self, caminho: str, n: Optional[int]) -> None:
        """
        Carrega linhas de um arquivo de texto após a linha n

        Args:
            caminho (str): Caminho do arquivo a ser carregado
            n (Optional[int]): Número da linha após a qual inserir, caso None, usa a corrente
        """

        if not os.path.isfile(caminho):
            print(f"  Erro: arquivo '{caminho}' não encontrado.")
            return

        if n is not None:
            ancora = self._obter_linha(n)

            if ancora is None and n != 0:
                print(f"  Erro: linha {n} não existe.")
                return
        
        else:
            ancora = self.corrente

        with open(caminho, "r", encoding="utf-8") as arq:
            linhas = arq.read().splitlines()

        ultima = ancora
        
        for texto in linhas:
            ultima = self._inserir_depois_do_no(ultima, texto)

        print(f"  {len(linhas)} linha(s) carregada(s) de '{caminho}'.")

    def cmd_salvar(self, caminho: str, i: Optional[int], f: Optional[int]) -> None:
        """
        Salva as linhas de i até f em um arquivo de texto

        Args:
            caminho (str): Caminho do arquivo de destino
            i (Optional[int]): Número da primeira linha a salvar
            f (Optional[int]): Número da última linha a salvar
        """

        inicio = i if i is not None else 1
        fim = f if f is not None else self.total_linhas
        linhas: List[str] = []

        for num in range(inicio, fim + 1):
            no = self._obter_linha(num)

            if no is None:
                print(f"  Erro: linha {num} não existe.")
                return
            
            linhas.append(no.texto)

        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write("\n".join(linhas))

        print(f"  {len(linhas)} linha(s) salva(s) em '{caminho}'.")

    def cmd_alterar(self, n: int) -> None:
        """
        Permite editar o conteúdo da linha n

        Args:
            n (int): Número da linha a alterar
        """

        no = self._obter_linha(n)

        if no is None:
            print(f"  Erro: linha {n} não existe.")
            return

        print(f"  Atual : {no.texto}")
        novo_texto = input("  Novo  : ")
        no.texto = novo_texto
        self.corrente = no
        print("  Linha alterada.")


def _parsear_comando(entrada: str) -> Tuple[str, List[str]]:
    """
    Separa a letra do comando dos seus argumentos

    Args:
        entrada (str): Linha digitada pelo usuário

    Returns:
        Tuple[str, List[str]]: Letra do comando em maiúsculo e lista de argumentos
    """

    partes = entrada.strip().split(None, 1)

    if not partes:
        return "", []

    cmd = partes[0].upper()
    args = [a.strip() for a in partes[1].split(",")] if len(partes) > 1 else []
    return cmd, args


def _para_int(valor: str) -> Optional[int]:
    """
    Converte uma string para inteiro, retornando None em caso de falha

    Args:
        valor (str): String a converter

    Returns:
        Optional[int]: Inteiro convertido ou None
    """

    try:
        return int(valor)

    except ValueError:
        return None


def executar_editor() -> None:
    """
    Inicia o loop principal do editor de texto, lendo e despachando comandos
    """

    editor = EditorTexto()
    print("\n  Editor de Texto  |  digite F para encerrar\n")

    while True:
        numero_corrente = editor._numero_corrente()
        indicador = f"[{numero_corrente}/{editor.total_linhas}]" if editor.total_linhas > 0 else "[vazio]"
        entrada = input(f"{indicador} => ").strip()

        if not entrada:
            continue

        cmd, args = _parsear_comando(entrada)

        if cmd == "F":
            print("\n  Editor encerrado.")
            break

        elif cmd == "I":
            n = _para_int(args[0]) if args else None
            editor.cmd_inserir(n)

        elif cmd == "E":
            i = _para_int(args[0]) if len(args) > 0 else None
            f = _para_int(args[1]) if len(args) > 1 else None
            editor.cmd_excluir(i, f)

        elif cmd == "D":
            if len(args) < 3:
                print("  Uso: D i,f,p")
                continue

            i, f, p = _para_int(args[0]), _para_int(args[1]), _para_int(args[2])
            
            if None in (i, f, p):
                print("  Erro: argumentos inválidos.")
                continue
            
            editor.cmd_duplicar(i, f, p)

        elif cmd == "L":
            i = _para_int(args[0]) if len(args) > 0 else None
            f = _para_int(args[1]) if len(args) > 1 else None
            editor.cmd_listar(i, f)

        elif cmd == "C":
            if not args:
                print("  Uso: C arq[,n]")
                continue
            
            caminho = args[0]
            n = _para_int(args[1]) if len(args) > 1 else None
            editor.cmd_carregar(caminho, n)

        elif cmd == "S":
            if not args:
                print("  Uso: S arq[,i[,f]]")
                continue
            
            caminho = args[0]
            i = _para_int(args[1]) if len(args) > 1 else None
            f = _para_int(args[2]) if len(args) > 2 else None
            editor.cmd_salvar(caminho, i, f)

        elif cmd == "A":
            n = _para_int(args[0]) if args else None
            
            if n is None:
                print("  Uso: A n")
                continue
            
            editor.cmd_alterar(n)

        else:
            print(f"  Comando desconhecido: '{cmd}'  (I, E, D, L, C, S, A, F)")


executar_editor()
