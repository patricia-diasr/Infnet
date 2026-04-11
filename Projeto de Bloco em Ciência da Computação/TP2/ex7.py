from typing import Dict, List, Union


def calcular_tamanho(pasta: Union[Dict, int], visitas: List[int]) -> int:
    """
    Calcula recursivamente o tamanho total ocupado por uma pasta e seus conteúdos

    Args:
        pasta (Union[Dict, int]): Pasta representada como dicionário aninhado ou arquivo representado como inteiro
        visitas (List[int]): Lista de um elemento usada como contador mutável de nós visitados

    Returns:
        int: Tamanho total em KB de todos os arquivos contidos na estrutura
    """

    visitas[0] += 1

    if isinstance(pasta, int):
        return pasta

    return sum(calcular_tamanho(conteudo, visitas) for _, conteudo in pasta.items())


def exibir_arvore(pasta: Union[Dict, int], nome: str = "raiz", nivel: int = 0) -> None:
    """
    Exibe a estrutura de pastas e arquivos em formato de árvore no terminal

    Args:
        pasta (Union[Dict, int]): Pasta representada como dicionário aninhado ou arquivo representado como inteiro
        nome (str): Nome do nó atual exibido na árvore
        nivel (int): Nível de profundidade atual, usado para calcular o recuo visual
    """

    recuo = "  " * nivel
    conector = "└─ " if nivel > 0 else ""

    if isinstance(pasta, int):
        print(f"{recuo}{conector}{nome}  ({pasta} KB)")
    else:
        print(f"{recuo}{conector}{nome}/")
        for filho, conteudo in pasta.items():
            exibir_arvore(conteudo, filho, nivel + 1)


def analisar_sistema_arquivos(sistema_arquivos: Dict, nome_raiz: str = "raiz") -> None:
    """
    Exibe a árvore de diretórios e calcula o tamanho total do sistema de arquivos

    Args:
        sistema_arquivos (Dict): Dicionário aninhado representando a estrutura de pastas
        nome_raiz (str): Nome exibido para o diretório raiz
    """

    visitas = [0]
    exibir_arvore(sistema_arquivos, nome_raiz)
    tamanho_total = calcular_tamanho(sistema_arquivos, visitas)

    print(f"\nNós visitados : {visitas[0]}")
    print(f"Tamanho total : {tamanho_total} KB")


sistema_arquivos = {
    "Documentos": {
        "Trabalho": {"projeto1.pdf": 500, "projeto2.pdf": 300},
        "Pessoal": {"receitas.txt": 10},
    },
    "Imagens": {
        "Ferias": {"foto1.jpg": 2000, "foto2.jpg": 3000},
        "logo.png": 150,
    },
    "README.txt": 5,
}

sistema_arquivos_2 = {
    "Projetos": {
        "Web": {
            "frontend": {
                "src": {"index.html": 12, "style.css": 34, "app.js": 210},
                "public": {"favicon.ico": 4, "robots.txt": 1},
            },
            "backend": {
                "api": {"routes.py": 88, "models.py": 120, "views.py": 95},
                "config": {"settings.py": 45, ".env": 2},
            },
        },
        "Mobile": {
            "android": {"MainActivity.java": 300, "build.gradle": 15},
            "ios": {"AppDelegate.swift": 280, "Info.plist": 8},
        },
        "DataScience": {
            "notebooks": {"analise.ipynb": 4500, "modelo.ipynb": 3200},
            "dados": {
                "brutos": {"dataset.csv": 51200, "labels.csv": 1024},
                "processados": {"features.npy": 20480, "targets.npy": 5120},
            },
            "modelos": {"modelo_final.pkl": 8192, "scaler.pkl": 64},
        },
    },
    "Midia": {
        "Musicas": {
            "Rock": {"faixa01.mp3": 8192, "faixa02.mp3": 7680},
            "Jazz": {"faixa01.flac": 40960, "faixa02.flac": 38400},
        },
        "Videos": {
            "Filmes": {"filme_a.mp4": 1474560, "filme_b.mkv": 2097152},
            "Series": {
                "Serie_A": {"ep01.mp4": 368640, "ep02.mp4": 376832},
                "Serie_B": {"ep01.mp4": 409600, "ep02.mp4": 417792},
            },
        },
        "Fotos": {
            "2023": {"janeiro": {"img001.jpg": 3500, "img002.jpg": 4100}},
            "2024": {"dezembro": {"img001.raw": 25600, "img002.raw": 24800}},
        },
    },
    "Backup": {
        "2023": {"backup_janeiro.zip": 204800, "backup_julho.zip": 307200},
        "2024": {"backup_janeiro.zip": 256000, "backup_completo.tar.gz": 512000},
    },
    "Sistema": {
        "logs": {"sistema.log": 2048, "erro.log": 512, "acesso.log": 1024},
        "temp": {"cache_a.tmp": 256, "cache_b.tmp": 128},
        "config": {"hosts": 1, "resolv.conf": 1, "fstab": 2},
    },
    "boot.ini": 1,
    "pagefile.sys": 8192,
}


print("\n===== Teste 1 - Sistema de arquivos 1 =====\n")
analisar_sistema_arquivos(sistema_arquivos, "disco")

print("\n\n===== Teste 2 - Sistema de arquivos 2 =====\n")
analisar_sistema_arquivos(sistema_arquivos_2, "disco2")
