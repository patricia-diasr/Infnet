import os


def percorrer_diretorio(caminho: str, nivel: int = 0) -> None:
    """
    Percorre recursivamente um diretório e seus subdiretórios, listando arquivos e pastas encontrados

    Args:
        caminho (str): Caminho do diretório a ser percorrido
        nivel (int): Nível de profundidade da recursão (usado para indentação)

    Returns:
        None
    """

    indentacao = "  " * nivel
    print(f"{indentacao}Diretório: {caminho}")

    try:
        itens = os.listdir(caminho)
    except Exception as e:
        print(f"{indentacao}Erro ao acessar {caminho}: {e}")
        return

    for item in itens:
        caminho_completo = os.path.join(caminho, item)

        if os.path.isdir(caminho_completo):
            print(f"{indentacao}📁 {item}")
            percorrer_diretorio(caminho_completo, nivel + 1)
        else:
            print(f"{indentacao}📄 {item}")


diretorios_teste = [
    ".",
    "..",
]
print("\n" + "=" * 40 + "\n")

for i, diretorio in enumerate(diretorios_teste):
    print(f"Teste {i+1}: Percorrendo diretório '{diretorio}'")

    percorrer_diretorio(diretorio)

    print("\n" + "=" * 40 + "\n")
