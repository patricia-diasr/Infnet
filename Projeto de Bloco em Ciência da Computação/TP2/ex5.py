from typing import Optional


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
    Editor de texto baseado em lista duplamente encadeada

    Attributes:
        primeira (Optional[Linha]): Ponteiro P, aponta para a primeira linha do texto
        corrente (Optional[Linha]): Ponteiro C, aponta para a linha atualmente selecionada
        total_linhas (int): Quantidade total de linhas no texto
    """

    def __init__(self) -> None:
        self.primeira: Optional[Linha] = None
        self.corrente: Optional[Linha] = None
        self.total_linhas: int = 0

    def inserir_depois(self, texto: str) -> None:
        """
        Insere uma nova linha imediatamente após a linha corrente

        Args:
            texto (str): Conteúdo textual da nova linha
        """

        nova = Linha(texto)

        if self.primeira is None:
            self.primeira = nova
            self.corrente = nova

        else:
            proxima = self.corrente.proximo
            nova.anterior = self.corrente
            nova.proximo = proxima
            self.corrente.proximo = nova

            if proxima is not None:
                proxima.anterior = nova

            self.corrente = nova

        self.total_linhas += 1

    def inserir_antes(self, texto: str) -> None:
        """
        Insere uma nova linha imediatamente antes da linha corrente

        Args:
            texto (str): Conteúdo textual da nova linha
        """

        nova = Linha(texto)

        if self.primeira is None:
            self.primeira = nova
            self.corrente = nova

        else:
            anterior = self.corrente.anterior
            nova.proximo = self.corrente
            nova.anterior = anterior
            self.corrente.anterior = nova

            if anterior is not None:
                anterior.proximo = nova

            else:
                self.primeira = nova

            self.corrente = nova

        self.total_linhas += 1

    def remover_corrente(self) -> Optional[str]:
        """
        Remove a linha corrente da lista e reposiciona o ponteiro corrente

        Returns:
            Optional[str]: Texto da linha removida, ou None se o editor estiver vazio
        """

        if self.corrente is None:
            return None

        texto_removido = self.corrente.texto
        anterior = self.corrente.anterior
        proxima = self.corrente.proximo

        if anterior is not None:
            anterior.proximo = proxima

        else:
            self.primeira = proxima

        if proxima is not None:
            proxima.anterior = anterior

        self.corrente = anterior if anterior is not None else proxima
        self.total_linhas -= 1

        return texto_removido

    def mover_para_cima(self) -> bool:
        """
        Move o ponteiro corrente uma linha acima

        Returns:
            bool: True se o movimento foi realizado, False se já está na primeira linha
        """

        if self.corrente is None or self.corrente.anterior is None:
            return False

        self.corrente = self.corrente.anterior
        return True

    def mover_para_baixo(self) -> bool:
        """
        Move o ponteiro corrente uma linha abaixo

        Returns:
            bool: True se o movimento foi realizado, False se já está na última linha
        """

        if self.corrente is None or self.corrente.proximo is None:
            return False

        self.corrente = self.corrente.proximo
        return True

    def ir_para_primeira(self) -> None:
        """Move o ponteiro corrente para a primeira linha do texto"""

        self.corrente = self.primeira

    def ir_para_ultima(self) -> None:
        """Move o ponteiro corrente para a última linha do texto"""

        atual = self.primeira

        while atual is not None and atual.proximo is not None:
            atual = atual.proximo
 
        self.corrente = atual

    def editar_corrente(self, novo_texto: str) -> bool:
        """
        Substitui o conteúdo da linha corrente pelo texto fornecido

        Args:
            novo_texto (str): Novo conteúdo da linha

        Returns:
            bool: True se a edição foi realizada, False se o editor estiver vazio
        """

        if self.corrente is None:
            return False

        self.corrente.texto = novo_texto
        return True

    def copiar_corrente_para_depois(self) -> bool:
        """
        Insere uma cópia da linha corrente imediatamente após ela mesma

        Returns:
            bool: True se a cópia foi realizada, False se o editor estiver vazio
        """

        if self.corrente is None:
            return False

        self.inserir_depois(self.corrente.anterior.texto if self.corrente.anterior else self.corrente.texto)
        return True

    def exibir_estrutura(self) -> None:
        """
        Exibe a representação visual da lista duplamente encadeada no terminal
        """

        if self.primeira is None:
            print("  (editor vazio)")
            return

        atual = self.primeira
        numero_linha = 1

        while atual is not None:
            e_primeira = atual is self.primeira
            e_corrente = atual is self.corrente
            e_ultima = atual.proximo is None

            prefixo_p = "P →" if e_primeira else "   "
            prefixo_c = "C →" if e_corrente else "   "

            link_ant = "[ ]" if atual.anterior is not None else "[X]"
            link_prx = "[ ]" if atual.proximo is not None else "[X]"

            print(f"{prefixo_p}  {prefixo_c}  {link_ant}{link_prx}  \"{atual.texto}\"")

            if not e_ultima:
                print(f"           ↓  ↑")

            numero_linha += 1
            atual = atual.proximo

    def exibir_texto(self) -> None:
        """Exibe o conteúdo do texto linha por linha, sem elementos estruturais"""

        if self.primeira is None:
            print("(editor vazio)")
            return

        atual = self.primeira

        while atual is not None:
            marcador = " ← corrente" if atual is self.corrente else ""
            print(f"{atual.texto}{marcador}")
            atual = atual.proximo


editor = EditorTexto()

for linha in ["A natureza,", "dizem-nos,", "é apenas o hábito...", "(Rousseau)"]:
    editor.inserir_depois(linha)


print("\n===== Teste 1 - Estrutura inicial após inserções =====\n")
editor.ir_para_primeira()
editor.exibir_estrutura()

print(f"\nTotal de linhas: {editor.total_linhas}")
print(f"Primeira linha: \"{editor.primeira.texto}\"")
print(f"Linha corrente: \"{editor.corrente.texto}\"")


print("\n\n===== Teste 2 - Navegação com ponteiro corrente =====\n")

editor.ir_para_primeira()
print(f"=> ir_para_primeira() -> corrente: \"{editor.corrente.texto}\"")

editor.mover_para_baixo()
print(f"=> mover_para_baixo() -> corrente: \"{editor.corrente.texto}\"")

editor.mover_para_baixo()
print(f"=> mover_para_baixo() -> corrente: \"{editor.corrente.texto}\"")

editor.mover_para_cima()
print(f"=> mover_para_cima() -> corrente: \"{editor.corrente.texto}\"")

editor.ir_para_ultima()
print(f"=> ir_para_ultima() -> corrente: \"{editor.corrente.texto}\"")

resultado = editor.mover_para_baixo()
print(f"=> mover_para_baixo() -> movimento realizado: {resultado} (já está na última linha)")


print("\n\n===== Teste 3 - Inserção antes e depois da corrente =====\n")

editor2 = EditorTexto()
editor2.inserir_depois("linha A")
editor2.inserir_depois("linha C")
editor2.ir_para_primeira()

print("=> Texto antes:")
editor2.exibir_texto()


print("\n=> Após inserir 'linha B' depois de 'linha A':")
editor2.inserir_depois("linha B")
editor2.exibir_texto()

print("\n=> Após inserir 'linha ZERO' antes da primeira linha:")
editor2.ir_para_primeira()
editor2.inserir_antes("linha ZERO")
editor2.exibir_texto()


print("\n\n===== Teste 4 - Edição e remoção da linha corrente =====\n")

editor3 = EditorTexto()
for linha in ["primeira", "segunda", "terceira"]:
    editor3.inserir_depois(linha)

editor3.ir_para_primeira()
editor3.mover_para_baixo()

print(f"Corrente antes de editar: \"{editor3.corrente.texto}\"")
editor3.editar_corrente("segunda (editada)")
print(f"Corrente após editar: \"{editor3.corrente.texto}\"")

removido = editor3.remover_corrente()
print(f"\n=> remover_corrente() -> removido: \"{removido}\"")
print(f"Corrente após remoção: \"{editor3.corrente.texto}\"")

print("\nEstado final:")
editor3.exibir_estrutura()
