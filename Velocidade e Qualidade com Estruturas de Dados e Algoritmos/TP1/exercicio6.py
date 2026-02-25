def quadrado_do_arroz(quantidade: int):
    """
    Calcula em qual quadrado do tabuleiro de xadrez uma determinada quantidade de grãos de arroz 
    será colocada, considerando que a quantidade de grãos dobra a cada quadrado

    Args:
        quantidade (int): Quantidade de grãos de arroz desejada

    Returns:
        int: Número do quadrado correspondente à quantidade de grãos
    """
    
    graos = 1
    quadrado = 1

    while graos < quantidade:
        graos *= 2
        quadrado += 1

    return quadrado


resultado = quadrado_do_arroz(16)
print("Quadrado:", resultado)
