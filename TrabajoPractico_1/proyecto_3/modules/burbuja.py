class Burbuja:
    def __init__(self, lista):
        self.__lista = lista

    def ordenar_lista(self):
        """Ordena la lista de manera ascendente usando burbuja."""
        contador = 0
        while contador < len(self.__lista):
            tamaño_lista = len(self.__lista) - contador
            for i in range(1, tamaño_lista):
                if self.__lista[i] < self.__lista[i - 1]:
                    aux = self.__lista[i]
                    self.__lista[i] = self.__lista[i - 1]
                    self.__lista[i - 1] = aux
            contador += 1
        return self.__lista

    def __str__(self):
        return f"{self.__lista}"
