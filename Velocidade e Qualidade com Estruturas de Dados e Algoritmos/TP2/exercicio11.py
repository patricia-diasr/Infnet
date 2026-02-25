class StackOverflowError(Exception):
    pass


class StackUnderflowError(Exception):
    pass


class Stack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.top = -1

    def push(self, value):
        if self.top >= self.capacity - 1:
            raise StackOverflowError("Erro: Stack Overflow (pilha cheia)")
        
        self.top += 1
        self.items[self.top] = value

    def pop(self):
        if self.top == -1:
            raise StackUnderflowError("Erro: Stack Underflow (pilha vazia)")
        
        value = self.items[self.top]
        self.items[self.top] = None
        self.top -= 1
        return value

    def peek(self):
        if self.top == -1:
            raise StackUnderflowError("Erro: Stack Underflow (pilha vazia)")
        return self.items[self.top]

    def is_empty(self):
        return self.top == -1

    def __str__(self):
        return f"Stack(top={self.top}, items={self.items})"
        
    
def inverter_string(texto):
    """
    Inverte uma string utilizando explicitamente uma pilha

    Args:
        texto (str): String que será invertida.

    Returns:
        str: String invertida.
    """
    
    pilha = Stack(len(texto))

    for caractere in texto:
        pilha.push(caractere)

    texto_invertido = ""

    while not pilha.is_empty():
        texto_invertido += pilha.pop()

    return texto_invertido
    
textos= [
    "Algoritmos",
    "Stack",
    "Python",
    "Velocidade e Qualidade com Estruturas de Dados e Algoritmos",
    "abcdefghijklmnopqrstuvwxyz",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
]

for i, texto in enumerate(textos):
    print(f"\n===== Teste {i+1} =====")
    print("Texto original:", texto)
    print("Texto invertido:", inverter_string(texto))
