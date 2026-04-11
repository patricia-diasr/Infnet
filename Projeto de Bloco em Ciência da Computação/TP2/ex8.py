def regua(n: int, inicio: int, fim: int) -> None:
    """
    Imprime recursivamente os traços de uma régua de ordem n no intervalo inicio e fim

    Args:
        n (int): Ordem da régua e comprimento do traço no ponto médio atual
        inicio (int): Início do intervalo atual
        fim (int): Fim do intervalo atual
    """

    if n == 0:
        return

    meio = (inicio + fim) // 2

    regua(n - 1, inicio, meio)
    print(f". {'─' * n}")
    regua(n - 1, meio, fim)


def imprimir_regua(n: int) -> None:
    """
    Imprime uma régua completa de ordem n no intervalo 0 e 2^n

    Args:
        n (int): Ordem da régua, define a profundidade e o intervalo 0 e 2^n
    """

    tamanho = 2 ** n

    print(f"Régua de ordem {n}  |  intervalo [0, {tamanho}]\n")
    print(".")
    regua(n, 0, tamanho)
    print(".")


print("\n===== Teste 1 - Régua de ordem 2 =====\n")
imprimir_regua(2)

print("\n\n===== Teste 2 - Régua de ordem 4 =====\n")
imprimir_regua(4)

print("\n\n===== Teste 3 - Régua de ordem 5 =====\n")
imprimir_regua(5)
