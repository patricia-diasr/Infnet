from typing import List
import math


def factor(x: int, lowest: int = 2) -> List[int]:
    """
    Realiza a fatoração de um número inteiro utilizando recursão

    Args:
        x (int): Número a ser fatorado
        lowest (int): Menor divisor a ser testado

    Returns:
        List[int]: Lista contendo os fatores de x
    """

    if x == 0:
        print("0 não possui fatoração definida.")
        return []

    if x == 1:
        return [1]

    if x < 0:
        return [-1] + factor(-x, lowest)

    limite = int(math.sqrt(x))

    for divisor in range(lowest, limite + 1):
        if x % divisor == 0:
            print(f"Divisor encontrado: {divisor} | {x} = {divisor} * {x // divisor}")
            return [divisor] + factor(x // divisor, divisor)

    print(f"{x} é primo.")
    return [x]


testes = [60, 97, 84, -45, 1, 0]
print("\n" + "=" * 40 + "\n")

for i, numero in enumerate(testes):
    print(f"Teste {i+1}: fatoração de {numero}" + "\n")

    fatores = factor(numero)

    print("Fatores:", fatores)
    print("\n" + "=" * 40 + "\n")
