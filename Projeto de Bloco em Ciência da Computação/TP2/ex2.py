import asyncio
import random
import time


ARQUIVOS_BLOQUEADOS = {"virus.exe", "malware.bat", "trojan.dll"}

LISTA_DOWNLOADS = [
    "relatorio_anual.pdf",
    "virus.exe",
    "musica_favorita.mp3",
    "backup_banco.sql",
    "apresentacao.pptx",
    "foto_viagem.jpg",
    "planilha_gastos.xlsx",
    "malware.bat",
    "codigo_fonte.zip",
    "manual_usuario.docx",
]


class ArquivoBloqueadoError(Exception):
    """
    Exceção lançada quando o download de um arquivo bloqueado é solicitado

    Attributes:
        nome_arquivo (str): Nome do arquivo que causou o bloqueio
    """

    def __init__(self, nome_arquivo: str) -> None:
        self.nome_arquivo = nome_arquivo
        super().__init__(f"Download bloqueado: '{nome_arquivo}' é um arquivo proibido")


async def baixar_arquivo(nome_arquivo: str) -> str:
    """
    Simula o download assíncrono de um arquivo com tempo de rede aleatório

    Args:
        nome_arquivo (str): Nome do arquivo a ser baixado

    Returns:
        str: Nome do arquivo baixado com sucesso
    """

    if nome_arquivo in ARQUIVOS_BLOQUEADOS:
        raise ArquivoBloqueadoError(nome_arquivo)

    duracao = random.uniform(1, 5)
    print(f"[INICIANDO ] {nome_arquivo:<30}  (estimado: {duracao:.1f}s)")

    await asyncio.sleep(duracao)
    print(f"[CONCLUÍDO ] {nome_arquivo:<30}  (durou: {duracao:.1f}s)")

    return nome_arquivo


async def main() -> None:
    """
    Ponto de entrada principal do gerenciador de downloads
    """

    print("\n===== Gerenciador de Downloads =====\n")
    print(f"Arquivos na fila: {len(LISTA_DOWNLOADS)}")
    print(f"Arquivos bloqueados: {ARQUIVOS_BLOQUEADOS}\n")
    print("---- Iniciando downloads ----\n")

    t_inicio = time.perf_counter()

    tarefas = [
        asyncio.create_task(baixar_arquivo(nome), name=nome)
        for nome in LISTA_DOWNLOADS
    ]

    resultados = await asyncio.gather(*tarefas, return_exceptions=True)

    t_fim = time.perf_counter()

    baixados = []
    bloqueados = []
    erros = []

    for nome, resultado in zip(LISTA_DOWNLOADS, resultados):
        if isinstance(resultado, ArquivoBloqueadoError):
            bloqueados.append(nome)

        elif isinstance(resultado, Exception):
            erros.append((nome, resultado))

        else:
            baixados.append(resultado)

    print("\n---- Relatório Final ----\n")
    print(f"Tempo total: {t_fim - t_inicio:.2f}s")
    print(f"Downloads concluídos: {len(baixados)}")
    print(f"Arquivos bloqueados: {len(bloqueados)}")
    print(f"Erros inesperados: {len(erros)}")

    if baixados:
        print("\nArquivos baixados com sucesso:")
        for nome in baixados:
            print(f"✅ {nome}")

    if bloqueados:
        print("\nArquivos bloqueados (não baixados):")
        for nome in bloqueados:
            print(f"❌ {nome}")

    if erros:
        print("\nErros inesperados:")
        for nome, exc in erros:
            print(f"! {nome} → {exc}")

    print()


asyncio.run(main())
