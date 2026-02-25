from typing import List

def extrair_caracteres_visiveis(texto: str) -> List[str]:
    """
    Remove os caracteres de espaço em branco de uma string

    Utiliza de list comprehension e o método `isspace()` para filtrar espaços, tabulações e quebras 
    de linha, retornando apenas os caracteres individuais restantes em uma lista

    Args:
        texto (str): String original a ser processada

    Returns:
        List[str]: Lista de strings, onde cada elemento é um caractere não-espaço da string original
    """
    
    return [char for char in texto if not char.isspace()]


frase = "Sítio do pica-pau amarelo \n 2023"
resultado = extrair_caracteres_visiveis(frase)

print(f"Frase original: {frase}\n")
print(f"Caracteres visiveis extraidos: {resultado}")
