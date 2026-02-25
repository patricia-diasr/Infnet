class QueueOverflowError(Exception):
    pass


class QueueUnderflowError(Exception):
    pass


class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            raise QueueOverflowError("Erro: Queue Overflow (fila cheia)")
        
        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = value
        self.size += 1

    def dequeue(self):
        if self.size == 0:
            raise QueueUnderflowError("Erro: Queue Underflow (fila vazia)")
        
        value = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value

    def __str__(self):
        return (f"Queue(front={self.front}, rear={self.rear}, "
                f"size={self.size}, items={self.items})")


print("=> Iniciando fila com capacidade 3")
queue = Queue(3)
print("Estado inicial:", queue)

print("\n=> Realizando enqueue e dequeue:")

queue.enqueue(10)
print("Após enqueue(10):", queue)
queue.enqueue(20)
print("Após enqueue(20):", queue)
queue.enqueue(30)
print("Após enqueue(30):", queue)
print("Dequeue:", queue.dequeue())
print("Após dequeue():", queue)
queue.enqueue(40)
print("Após enqueue(40):", queue)
print("Dequeue:", queue.dequeue())
print("Após dequeue():", queue)
print("Dequeue:", queue.dequeue())
print("Após dequeue():", queue)
print("Dequeue:", queue.dequeue())
print("Após dequeue():", queue)
