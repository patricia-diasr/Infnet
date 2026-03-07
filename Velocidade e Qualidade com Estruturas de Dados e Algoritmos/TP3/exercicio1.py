from typing import Tuple


def mult(x: int, y: int, nivel: int = 0) -> int:
    """
    Calcula a multiplicação entre dois inteiros utilizando apenas soma e recursão

    Args:
        x (int): Primeiro número da multiplicação
        y (int): Segundo número da multiplicação (quantidade de somas)
        nivel (int): Nível da chamada recursiva (usado apenas para visualização)

    Returns:
        int: Resultado da multiplicação
    """

    indentacao = "  " * nivel
    print(f"{indentacao}Chamada: mult({x}, {y})")

    if y == 0:
        print(f"{indentacao}Retorno (caso base): 0")
        return 0

    resultado_parcial = mult(x, y - 1, nivel + 1)
    resultado = x + resultado_parcial
    print(f"{indentacao}Retorno: {x} + {resultado_parcial} = {resultado}")

    return resultado


testes = [
    (3, 4),
    (5, 3),
    (7, 2),
    (4, 5)
]

print("\n" + "=" * 40 + "\n")
for i, (x, y) in enumerate(testes):
    print(f"Teste {i+1}: {x} x {y}" + "\n")
    resultado = mult(x, y)

    print(f"\nResultado final: {resultado}")
    print("\n" + "=" * 40 + "\n")
