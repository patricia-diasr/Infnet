from typing import Union


def power(x: float, y: int, nivel: int = 0) -> float:
    """
    Calcula x elevado a y utilizando recursão

    Args:
        x (float): Base da potência
        y (int): Expoente
        nivel (int): Nível da chamada recursiva (apenas para visualização)

    Returns:
        float: Resultado de x elevado a y
    """

    indentacao = "  " * nivel
    print(f"{indentacao}Chamada: power({x}, {y})")

    if y == 0:
        print(f"{indentacao}Retorno (caso base): 1")
        return 1

    if y == 1:
        print(f"{indentacao}Retorno (caso base): {x}")
        return x

    if y < 0:
        print(f"{indentacao}Transformação: 1 / power({x}, {-y})")
        resultado = 1 / power(x, -y, nivel + 1)
        print(f"{indentacao}Retorno: {resultado}")
        return resultado

    resultado_parcial = power(x, y - 1, nivel + 1)
    resultado = x * resultado_parcial
    print(f"{indentacao}Retorno: {x} * {resultado_parcial} = {resultado}")

    return resultado


testes = [
    (2, 3),
    (5, 2),
    (4, 0),
    (2, -3),
    (10, 1)
]
print("\n" + "=" * 40 + "\n")

for i, (base, expoente) in enumerate(testes):
    print(f"Teste {i+1}: {base}^{expoente}")

    resultado = power(base, expoente)

    print(f"\nResultado final: {resultado}")
    print("\n" + "=" * 40 + "\n")
