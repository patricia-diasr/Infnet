from typing import List, Optional, Tuple
import unicodedata


class DicionarioErroChaveNaoEncontrada(Exception):
    """Levantada ao buscar ou remover uma chave inexistente no dicionario"""


class DicionarioErroChaveDuplicada(Exception):
    """Levantada ao tentar inserir uma chave que ja existe no dicionario"""


class NodoAVL:
    """
    Nodo de uma arvore AVL que armazena um par chave-valor

    Attributes:
        chave (str): Palavra do verbete normalizada para comparacao
        chave_original (str): Palavra do verbete com grafia original
        valor (List[str]): Lista de significados associados a palavra
        altura (int): Altura do nodo na arvore, usada para calculo do fator de balanceamento
        esquerda (Optional[NodoAVL]): Filho esquerdo
        direita (Optional[NodoAVL]): Filho direito
    """


    def __init__(self, chave: str, valor: str) -> None:
        self.chave: str = _normalizar(chave)
        self.chave_original: str = chave
        self.valor: List[str] = [valor]
        self.altura: int = 1
        self.esquerda: Optional[NodoAVL] = None
        self.direita: Optional[NodoAVL] = None


    def __repr__(self) -> str:
        return f"NodoAVL(chave={self.chave_original!r}, altura={self.altura})"


def _normalizar(chave: str) -> str:
    """
    Normaliza uma string para comparacao lexicografica sem distincao de case ou acentos

    Args:
        chave (str): Palavra a ser normalizada

    Returns:
        str: Palavra em letras minusculas e sem acentos
    """

    sem_acento = unicodedata.normalize("NFD", chave)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.lower()


def _altura(nodo: Optional[NodoAVL]) -> int:
    """
    Retorna a altura de um nodo ou zero se o nodo for None

    Args:
        nodo (Optional[NodoAVL]): Nodo a ser consultado

    Returns:
        int: Altura do nodo
    """

    return nodo.altura if nodo else 0


def _atualizar_altura(nodo: NodoAVL) -> None:
    """
    Recalcula e atualiza o atributo altura de um nodo com base nos seus filhos

    Args:
        nodo (NodoAVL): Nodo a ter a altura atualizada
    """

    nodo.altura = 1 + max(_altura(nodo.esquerda), _altura(nodo.direita))


def _fator_balanceamento(nodo: NodoAVL) -> int:
    """
    Calcula o fator de balanceamento de um nodo

    Args:
        nodo (NodoAVL): Nodo a ser avaliado

    Returns:
        int: Diferenca entre a altura do filho esquerdo e do filho direito
    """

    return _altura(nodo.esquerda) - _altura(nodo.direita)


def _rotacao_direita(y: NodoAVL) -> NodoAVL:
    """
    Executa uma rotacao simples para a direita em torno do nodo y

    Args:
        y (NodoAVL): Nodo desbalanceado que sera rotacionado

    Returns:
        NodoAVL: Nova raiz apos a rotacao
    """

    x = y.esquerda
    t2 = x.direita

    x.direita = y
    y.esquerda = t2

    _atualizar_altura(y)
    _atualizar_altura(x)

    return x


def _rotacao_esquerda(x: NodoAVL) -> NodoAVL:
    """
    Executa uma rotacao simples para a esquerda em torno do nodo x

    Args:
        x (NodoAVL): Nodo desbalanceado que sera rotacionado

    Returns:
        NodoAVL: Nova raiz apos a rotacao
    """

    y = x.direita
    t2 = y.esquerda

    y.esquerda = x
    x.direita = t2

    _atualizar_altura(x)
    _atualizar_altura(y)

    return y


def _rebalancear(nodo: NodoAVL) -> NodoAVL:
    """
    Verifica e corrige o balanceamento de um nodo aplicando rotacoes simples ou duplas

    Args:
        nodo (NodoAVL): Nodo a ser rebalanceado

    Returns:
        NodoAVL: Raiz da subarvore apos o rebalanceamento
    """

    _atualizar_altura(nodo)
    fb = _fator_balanceamento(nodo)

    if fb > 1:
        if _fator_balanceamento(nodo.esquerda) < 0:
            nodo.esquerda = _rotacao_esquerda(nodo.esquerda)

        return _rotacao_direita(nodo)

    if fb < -1:
        if _fator_balanceamento(nodo.direita) > 0:
            nodo.direita = _rotacao_direita(nodo.direita)

        return _rotacao_esquerda(nodo)

    return nodo


def _minimo(nodo: NodoAVL) -> NodoAVL:
    """
    Retorna o nodo com a menor chave em uma subarvore

    Args:
        nodo (NodoAVL): Raiz da subarvore

    Returns:
        NodoAVL: Nodo com a menor chave
    """

    atual = nodo

    while atual.esquerda:
        atual = atual.esquerda

    return atual


def _inserir(nodo: Optional[NodoAVL], chave: str, valor: str) -> NodoAVL:
    """
    Insere um par chave-valor na subarvore e rebalanceia o caminho de retorno

    Args:
        nodo (Optional[NodoAVL]): Raiz da subarvore atual
        chave (str): Chave normalizada do verbete
        valor (str): Significado a ser associado

    Returns:
        NodoAVL: Raiz da subarvore apos a insercao e rebalanceamento

    Raises:
        DicionarioErroChaveDuplicada: Se a chave ja existir na arvore
    """

    chave_norm = _normalizar(chave)

    if nodo is None:
        return NodoAVL(chave, valor)

    if chave_norm < nodo.chave:
        nodo.esquerda = _inserir(nodo.esquerda, chave, valor)

    elif chave_norm > nodo.chave:
        nodo.direita = _inserir(nodo.direita, chave, valor)

    else:
        raise DicionarioErroChaveDuplicada(f"Verbete '{chave}' ja existe no dicionario")

    return _rebalancear(nodo)


def _buscar(nodo: Optional[NodoAVL], chave: str) -> NodoAVL:
    """
    Busca um nodo pela chave na subarvore

    Args:
        nodo (Optional[NodoAVL]): Raiz da subarvore atual
        chave (str): Chave normalizada do verbete

    Returns:
        NodoAVL: Nodo encontrado

    Raises:
        DicionarioErroChaveNaoEncontrada: Se a chave nao for encontrada
    """

    chave_norm = _normalizar(chave)

    if nodo is None:
        raise DicionarioErroChaveNaoEncontrada(f"Verbete '{chave}' nao encontrado no dicionario")

    if chave_norm == nodo.chave:
        return nodo

    elif chave_norm < nodo.chave:
        return _buscar(nodo.esquerda, chave)

    else:
        return _buscar(nodo.direita, chave)


def _remover(nodo: Optional[NodoAVL], chave: str) -> Optional[NodoAVL]:
    """
    Remove o nodo com a chave informada da subarvore e rebalanceia o caminho de retorno

    Args:
        nodo (Optional[NodoAVL]): Raiz da subarvore atual
        chave (str): Chave normalizada do verbete a ser removido

    Returns:
        Optional[NodoAVL]: Raiz da subarvore apos a remocao e rebalanceamento

    Raises:
        DicionarioErroChaveNaoEncontrada: Se a chave nao for encontrada
    """

    chave_norm = _normalizar(chave)

    if nodo is None:
        raise DicionarioErroChaveNaoEncontrada(f"Verbete '{chave}' nao encontrado no dicionario")

    if chave_norm < nodo.chave:
        nodo.esquerda = _remover(nodo.esquerda, chave)

    elif chave_norm > nodo.chave:
        nodo.direita = _remover(nodo.direita, chave)

    else:
        if nodo.esquerda is None:
            return nodo.direita

        elif nodo.direita is None:
            return nodo.esquerda

        sucessor = _minimo(nodo.direita)
        nodo.chave = sucessor.chave
        nodo.chave_original = sucessor.chave_original
        nodo.valor = sucessor.valor
        nodo.direita = _remover(nodo.direita, sucessor.chave_original)

    return _rebalancear(nodo)


def _inorder(nodo: Optional[NodoAVL], resultado: List[Tuple[str, List[str]]]) -> None:
    """
    Percorre a arvore em ordem e acumula pares (chave_original, valor) no resultado

    Args:
        nodo (Optional[NodoAVL]): Nodo atual do percurso
        resultado (List[Tuple[str, List[str]]]): Lista acumuladora de pares chave-valor
    """

    if nodo is None:
        return

    _inorder(nodo.esquerda, resultado)
    resultado.append((nodo.chave_original, nodo.valor))
    _inorder(nodo.direita, resultado)


class DicionarioAVL:
    """
    Dicionario de verbetes implementado sobre uma arvore AVL com indice remissivel

    Attributes:
        _raiz (Optional[NodoAVL]): Raiz da arvore AVL
        _tamanho (int): Numero de verbetes armazenados
        _indice_remissivo (dict): Mapa de sinonimos e termos relacionados para chaves do dicionario
    """

    def __init__(self) -> None:
        self._raiz: Optional[NodoAVL] = None
        self._tamanho: int = 0
        self._indice_remissivo: dict = {}

    def inserir(self, chave: str, valor: str, remissoes: Optional[List[str]] = None) -> None:
        """
        Insere um verbete e seu significado no dicionario, com remissoes opcionais

        Args:
            chave (str): Palavra do verbete
            valor (str): Significado da palavra
            remissoes (Optional[List[str]]): Lista de termos que devem apontar para esta chave

        Raises:
            DicionarioErroChaveDuplicada: Se o verbete ja existir
        """

        self._raiz = _inserir(self._raiz, chave, valor)
        self._tamanho += 1

        if remissoes:
            for termo in remissoes:
                self._indice_remissivo[_normalizar(termo)] = chave

    def adicionar_significado(self, chave: str, valor: str) -> None:
        """
        Adiciona um significado adicional a um verbete ja existente

        Args:
            chave (str): Palavra do verbete
            valor (str): Novo significado a ser adicionado

        Raises:
            DicionarioErroChaveNaoEncontrada: Se o verbete nao existir
        """

        nodo = _buscar(self._raiz, chave)
        nodo.valor.append(valor)

    def buscar(self, chave: str) -> Tuple[str, List[str]]:
        """
        Busca um verbete pelo nome e retorna sua chave original e lista de significados

        Args:
            chave (str): Palavra a ser buscada

        Returns:
            Tuple[str, List[str]]: Par (chave_original, lista_de_significados)

        Raises:
            DicionarioErroChaveNaoEncontrada: Se o verbete nao existir
        """

        chave_norm = _normalizar(chave)

        if chave_norm in self._indice_remissivo:
            chave = self._indice_remissivo[chave_norm]

        nodo = _buscar(self._raiz, chave)
        return nodo.chave_original, nodo.valor

    def remover(self, chave: str) -> None:
        """
        Remove um verbete do dicionario e suas remissoes associadas

        Args:
            chave (str): Palavra do verbete a ser removido

        Raises:
            DicionarioErroChaveNaoEncontrada: Se o verbete nao existir
        """

        _buscar(self._raiz, chave)
        self._raiz = _remover(self._raiz, chave)
        self._tamanho -= 1

        chave_norm = _normalizar(chave)
        self._indice_remissivo = {
            k: v for k, v in self._indice_remissivo.items()
            if _normalizar(v) != chave_norm
        }

    def listar(self) -> List[Tuple[str, List[str]]]:
        """
        Retorna todos os verbetes em ordem alfabetica

        Returns:
            List[Tuple[str, List[str]]]: Lista de pares (chave_original, lista_de_significados)
        """

        resultado: List[Tuple[str, List[str]]] = []
        _inorder(self._raiz, resultado)
        return resultado

    def altura(self) -> int:
        """
        Retorna a altura atual da arvore AVL

        Returns:
            int: Altura da arvore, ou zero se vazia
        """

        return _altura(self._raiz)

    def tamanho(self) -> int:
        """
        Retorna o numero de verbetes armazenados no dicionario

        Returns:
            int: Numero de verbetes
        """

        return self._tamanho

    def listar_remissoes(self) -> List[Tuple[str, str]]:
        """
        Retorna todos os pares de remissao (termo_remissivo, chave_destino) cadastrados

        Returns:
            List[Tuple[str, str]]: Lista de pares (termo, chave_destino)
        """

        return [(termo, destino) for termo, destino in self._indice_remissivo.items()]

    def __repr__(self) -> str:
        return f"DicionarioAVL(tamanho={self._tamanho}, altura={self.altura()})"


dic = DicionarioAVL()

verbetes = [
    ("Catarse", "Processo de purificacao emocional experimentado pelo leitor ou espectador diante de uma obra tragica, conceito originado na Poetica de Aristoteles"),
    ("Romantasia", "Subgênero que mescla elementos de fantasia épica com um romance central obrigatório e final feliz."),
    ("Epiteto", "Adjetivo ou locucao adjetiva que caracteriza de forma expressiva um substantivo, muito presente na epopeia homerica"),
    ("Dark Romance", "Subgênero do romance que explora temas sombrios, tabus e relacionamentos moralmente cinzentos."),
    ("Quixotesco", "Relativo ao espirito idealista e visionario de Dom Quixote, personagem de Miguel de Cervantes, que luta contra moinhos de vento"),
    ("Enemies to Lovers", "Tropo narrativo onde os protagonistas começam como rivais ou inimigos e desenvolvem um relacionamento amoroso."),
    ("Hamartia", "Falha tragica ou erro de julgamento do heroi que leva a sua ruina, conceito aristotelico presente em obras como Edipo Rei"),
    ("Found Family", "Tropo focado em um grupo de personagens sem laços sanguíneos que formam um vínculo familiar profundo."),
    ("Kafkiano", "Adjetivo que descreve situacoes absurdas, burocraticas e opressivas, inspirado na obra de Franz Kafka"),
    ("Worldbuilding", "Processo de construção de um universo fictício detalhado, incluindo leis de magia, política e cultura."),
    ("Leitmotiv", "Tema ou motivo recorrente em uma obra literaria ou musical que representa um personagem, ideia ou situacao"),
    ("Slow Burn", "Narrativa onde o romance se desenvolve de forma muito lenta, focando na tensão acumulada."),
    ("Mimese", "Imitacao ou representacao da realidade na arte e na literatura, conceito central na Poetica de Aristoteles"),
    ("Grimdark", "Subgênero da fantasia marcado por um tom amoral, violento, realista e pessimista."),
    ("Narrador", "Instancia textual responsavel por contar a historia, podendo ser em primeira ou terceira pessoa"),
    ("Cottagecore", "Estética literaria que idealiza a vida rural, a natureza, a simplicidade e o aconchego."),
    ("Onomatopeia", "Figura de linguagem em que a palavra imita o som do que representa"),
    ("Cliffhanger", "Recurso que termina um capítulo ou livro em um momento de suspense extremo para prender o leitor."),
    ("Pastiche", "Obra literaria que imita o estilo de outro autor ou epoca, podendo ter carater de homenagem ou parodi"),
    ("Comfort Book", "Livro que o leitor revisita para se sentir bem, geralmente com uma trama acolhedora."),
    ("Quimera", "Ser mitologico hibrido que representa um sonho irrealizavel, referenciado por Dante na Divina Comedia"),
    ("Trope", "Padrão, motivo ou clichê narrativo reconhecível que se repete dentro de um gênero."),
    ("Rapsodo", "Poeta ou recitador ambulante da Grecia Antiga que declamava poemas epicos, como os de Homero"),
    ("Spicy", "Termo usado para classificar livros com conteúdo erótico explícito ou cenas detalhadas."),
    ("Sublime", "Categoria estetica que designa o que provoca admiracao e terror simultaneamente, explorada por Burke e Kant"),
    ("POV (Point of View)", "Perspectiva pela qual a história é contada, como o 'Dual POV' alternado."),
    ("Tragedia", "Genero dramatico de origem grega que encena a queda de um heroi por sua hamartia, teorizado por Aristoteles"),
    ("Urban Fantasy", "Fantasia ambientada em um cenário urbano contemporâneo e real."),
    ("Utopia", "Sociedade ideal e perfeita imaginada por Thomas More em sua obra homonima de 1516"),
    ("YA (Young Adult)", "Literatura voltada para o público jovem adulto, focando em temas de amadurecimento."),
    ("Verossimilhanca", "Qualidade do que parece verdadeiro dentro de uma obra ficcional, criterio de coerencia narrativa"),
    ("NA (New Adult)", "Categoria que foca na transição para a vida adulta, com temas mais maduros que o YA."),
    ("Aforismo", "Frase curta e incisiva que exprime uma verdade geral ou maxima de sabedoria"),
    ("Retelling", "Reescrita de um conto de fadas, mito ou clássico sob uma nova perspectiva."),
    ("Bildungsroman", "Subgenero romanesco que narra o desenvolvimento moral e psicologico do protagonista desde a juventude"),
    ("Magic System", "O conjunto de regras que define como a magia funciona em um mundo de fantasia."),
    ("Cronotopo", "Conceito de Bakhtin que designa a integracao de tempo e espaco como elemento constitutivo do genero"),
    ("BookTok", "Comunidade de leitores no TikTok que dita tendências e viraliza títulos."),
    ("Dialogismo", "Principio teorizado por Bakhtin segundo o qual todo texto e constituido pela relacao com outros discursos"),
    ("Plot Twist", "Mudança radical e inesperada na direção da história que altera a percepção do leitor."),
    ("Ekphrasis", "Descricao literaria detalhada de uma obra de arte visual, como o escudo de Aquiles"),
    ("Unreliable Narrator", "Narrador cujas falas ou percepções são suspeitas, forçando o leitor a duvidar da verdade."),
    ("Fabula", "Narrativa curta de carater moral protagonizada por animais, popularizada por Esopo"),
    ("Dystopia", "Sociedade imaginária opressiva, geralmente sob controle totalitário."),
    ("Grotesco", "Categoria estetica que combina elementos horriveis e comicos, presente em Rabelais"),
    ("Steampunk", "Passado alternativo onde a tecnologia a vapor evoluiu de forma avançada."),
    ("Hermeneutica", "Arte e teoria da interpretacao de textos, originalmente aplicada a textos sagrados"),
    ("Cyberpunk", "Ficção científica focada em tecnologia avançada e baixa qualidade de vida."),
    ("Intertextualidade", "Relacao entre textos em que um dialoga, cita ou transforma outro, conceito de Julia Kristeva"),
    ("Hype", "Estado de entusiasmo exagerado em torno de um lançamento literário."),
    ("Janela indiscreta", "Metafora da narrativa em que o narrador ou personagem observa o mundo de forma voyeuristica"),
    ("ARC (Advance Review Copy)", "Cópia avançada enviada para resenhas antes do lançamento oficial."),
    ("Katharsis", "Transliteracao alternativa de catarse, purificacao emocional pela experiencia tragica"),
    ("TBR (To Be Read)", "Sigla para a lista de livros que o leitor pretende ler."),
    ("Lirismo", "Qualidade de uma obra literaria marcada pela subjetividade e expressao de sentimentos intimos"),
    ("Grumpy x Sunshine", "Dinâmica de personagens onde um é mal-humorado e o outro é muito alegre."),
    ("Metalinguagem", "Uso da linguagem para falar sobre a propria linguagem, recurso da literatura moderna"),
    ("Fake Dating", "Tropo onde personagens fingem um namoro e acabam se apaixonando de verdade."),
    ("Neologismo", "Palavra nova criada para designar conceitos novos"),
    ("He Who Falls First", "Quando o protagonista masculino se apaixona antes da protagonista feminina."),
    ("Cozy Mystery", "Mistério leve, sem violência explícita, geralmente em vilarejos charmosos."),
    ("Space Opera", "Ficção científica épica focada em política e batalhas espaciais."),
    ("Magical Realism", "Gênero onde elementos mágicos são parte natural de um mundo realista."),
    ("Canon", "Fatos e histórias oficialmente reconhecidos como parte de um universo fictício."),
    ("Fandom", "Comunidade de fãs de uma determinada obra ou autor."),
    ("Fanfiction", "Histórias criadas por fãs baseadas em universos já existentes."),
    ("Mary Sue / Gary Stu", "Personagem idealizado demais, sem defeitos e que resolve tudo facilmente."),
    ("Show, Don't Tell", "Técnica de escrita que foca em mostrar ações em vez de apenas explicá-las."),
    ("Stream of Consciousness", "Técnica que reproduz o fluxo desordenado de pensamentos de um personagem."),
    ("Trigger Warning", "Aviso sobre conteúdos sensíveis que podem causar desconforto ou gatilhos."),
    ("Instalove", "Tropo onde o casal se apaixona instantaneamente sem construção gradual."),
    ("Ship", "Ato de torcer pelo relacionamento amoroso entre dois personagens."),
    ("Soft Magic", "Sistema de magia sem regras explicadas, focado no maravilhamento."),
    ("Hard Magic", "Sistema de magia com regras e limitações muito bem definidas."),
    ("Morally Grey", "Personagem cujas ações e bússola moral são ambíguas."),
    ("Epílogo", "Seção final que mostra o que aconteceu após a conclusão da trama principal."),
    ("Prólogo", "Texto introdutório que prepara o cenário ou a história pregressa."),
    ("Easter Egg", "Pequena referência ou detalhe escondido para fãs atentos."),
    ("Beta Reader", "Pessoa que lê o livro antes de publicado para oferecer críticas construtivas."),
    ("Ghostwriter", "Escritor contratado para redigir uma obra que será assinada por outra pessoa.")
]

remissoes_verbetes = {
    "Catarse": ["purificacao", "catharsis aristotelica"],
    "Quixotesco": ["dom quixote", "idealismo"],
    "Hamartia": ["falha tragica", "erro do heroi"],
    "Kafkiano": ["kafka", "absurdo"],
    "Leitmotiv": ["motivo recorrente", "tema musical"],
    "Mimese": ["imitacao", "representacao"],
    "Utopia": ["thomas more", "sociedade ideal"],
    "Bildungsroman": ["romance de formacao", "romance de aprendizado"],
    "Intertextualidade": ["kristeva", "dialogismo textual"],
    "Katharsis": ["catarse"],
}

for chave, valor in verbetes:
    remissoes = remissoes_verbetes.get(chave)
    dic.inserir(chave, valor, remissoes=remissoes)

dic.adicionar_significado("Tragedia", "Modalidade literaria que explora conflitos humanos irresolutos levando o protagonista a um desfecho fatal")
dic.adicionar_significado("Narrador", "Em narratologia moderna, distingue-se entre narrador confiavel e narrador nao confiavel")


print("\n===== Teste 1 - Estado Inicial da Arvore =====\n")
print(f"Verbetes inseridos: {dic.tamanho()}")
print(f"Altura da arvore: {dic.altura()}")
print(f"Representacao: {dic}\n")


print("\n===== Teste 2 - Busca de Verbetes =====\n")
buscas = ["Catarse", "Tragedia", "kafkiano", "UTOPIA", "Bildungsroman", "Narrador", "Ekphrasis"]

for termo in buscas:
    chave_orig, significados = dic.buscar(termo)
    print(f"Termo buscado: '{termo}'")
    print(f"Chave original: '{chave_orig}'")
    for i, sig in enumerate(significados, 1):
        print(f"=> Significado {i}: {sig}")
    print()


print("\n===== Teste 3 - Busca via Indice Remissivo =====\n")
remissoes_teste = ["purificacao", "falha tragica", "romance de formacao", "kafka"]

for termo in remissoes_teste:
    chave_orig, significados = dic.buscar(termo)
    print(f"Remissao '{termo}' -> verbete '{chave_orig}'")
    print(f"=> Significado: {significados[0]}")
    print()


print("\n===== Teste 4 - Listagem Ordenada (Inorder) =====\n")
todos = dic.listar()
print(f"{'#':>3}  {'Verbete':<30}  {'Qtd. Significados':>18}")
print(f"{'-'*3}  {'-'*30}  {'-'*18}")
for i, (chave, valores) in enumerate(todos, 1):
    print(f"{i:>3}  {chave:<30}  {len(valores):>18}")
print()


print("\n===== Teste 5 - Remocao de Verbetes =====\n")
remover = ["Katharsis", "Janela indiscreta", "Onomatopeia"]

for termo in remover:
    dic.remover(termo)
    print(f"Removido: '{termo}'")

print(f"\nVerbetes apos remocao: {dic.tamanho()}")
print(f"Altura apos remocao: {dic.altura()}")
print()

try:
    dic.buscar("Katharsis")
except DicionarioErroChaveNaoEncontrada as e:
    print(f"Busca apos remocao -> excecao esperada: {e}")
print()


print("\n===== Teste 6 - Erro ao Inserir Duplicata =====\n")
try:
    dic.inserir("Catarse", "Definicao duplicada")
except DicionarioErroChaveDuplicada as e:
    print(f"Excecao esperada: {e}\n")


print("\n===== Teste 7 - Indice Remissivo Cadastrado =====\n")
remissoes = dic.listar_remissoes()
print(f"{'Termo remissivo':<30}  {'Aponta para':<20}")
print(f"{'-'*30}  {'-'*20}")
for termo, destino in sorted(remissoes):
    print(f"{termo:<30}  {destino:<20}")
print()


print("\n===== Teste 8 - Altura e Tamanho Finais =====\n")
print(f"Tamanho final: {dic.tamanho()} verbetes")
print(f"Altura final: {dic.altura()}")
print(f"Representacao: {dic}\n")
