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


print("=> Iniciando pilha com capacidade 3")
stack = Stack(3)
print("Estado inicial:", stack)

print("\n=> Realizando push:")
stack.push(10)
print("Após push(10):", stack)
stack.push(20)
print("Após push(20):", stack)
stack.push(30)
print("Após push(30):", stack)

print("\n=>Testando overflow:")
try:
    stack.push(40)
except Exception as e:
    print("Tentativa de push(40):", e)

print("\n=> Realizando pop:")
print("Pop:", stack.pop())
print("Após pop():", stack)
print("Pop:", stack.pop())
print("Após pop():", stack)
print("Pop:", stack.pop())
print("Após pop():", stack)

print("\n=> Testando underflow:")
try:
    stack.pop()
except Exception as e:
    print("Tentativa de pop():", e)
