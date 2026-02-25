from typing import List
import random

class Array:
    def __init__(self, tamanho: int):
        """
        Inicializa a estrutura de dados com um tamanho definido

        Args:
            tamanho (int): Número máximo de elementos do array
        """
        
        self.__a: List[int] = []
        self.__nItems: int = 0
        self.__tamanho: int = tamanho

    def insert(self, valor: int) -> None:
        """
        Insere um valor inteiro no array

        Args:
            valor (int): Valor a ser inserido
        """
        
        if self.__nItems < self.__tamanho:
            self.__a.append(valor)
            self.__nItems += 1

    def swap(self, i: int, j: int) -> None:
        """
        Troca a posição de dois elementos no array.

        Args:
            i (int): Índice do primeiro elemento
            j (int): Índice do segundo elemento
        """
        self.__a[i], self.__a[j] = self.__a[j], self.__a[i]

    def bubbleSort(self) -> None:
        """
        Ordena os elementos do array utilizando o algoritmo Bubble Sort bidirecional

        O algoritmo percorre o array em duas direções:
        - Da esquerda para a direita, levando o maior elemento para a direita
        - Da direita para a esquerda, levando o menor elemento para a esquerda

        Dois índices externos são utilizados:
        - left: limite inferior da área não ordenada
        - right: limite superior da área não ordenada

        A cada iteração completa, esses limites são ajustados, reduzindo a região ainda não 
        ordenada
        """

        left = 0
        right = self.__nItems - 1

        while left < right:
            # Da esquerda para a direita
            for inner in range(left, right):
                if self.__a[inner] > self.__a[inner + 1]:
                    self.swap(inner, inner + 1)
            right -= 1

            # Da direita para a esquerda
            for inner in range(right, left, -1):
                if self.__a[inner] < self.__a[inner - 1]:
                    self.swap(inner, inner - 1)
            left += 1

    def get_array(self) -> List[int]:
        """
        Retorna uma cópia do array interno

        Returns:
            List[int]: Lista com os elementos do array
        """
        
        return self.__a.copy()


array = Array(20)
numeros = list(range(1, 21))
random.shuffle(numeros)

for numero in numeros:
    array.insert(numero)

print("Números embaralhados:")
print(array.get_array())

array.bubbleSort()
print("\nNúmeros ordenados:")
print(array.get_array())
