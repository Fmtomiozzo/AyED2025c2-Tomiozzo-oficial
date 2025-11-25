class Radix_sort:
    def __init__(self, lista):
        # Inicializa la clase con una lista de números.
        self.__lista = lista

    def ordenar(self):
        # Determina la cantidad máxima de dígitos en los números de la lista.
        cantidad_de_digitos = 0
        for elemento in self.__lista:
            digitos = len(str(elemento))
            if digitos > cantidad_de_digitos:
                cantidad_de_digitos = digitos

        # Normaliza la lista de números como cadenas con ceros a la izquierda.
        lista_normalizada = [
            str(elemento).zfill(cantidad_de_digitos) for elemento in self.__lista
        ]

        # Recorre cada posición de dígito desde el menos significativo al más significativo.
        for posicion in range(cantidad_de_digitos - 1, -1, -1):
            # Crea 10 "baldes", uno por cada dígito 0-9
            lista_auxiliar = [[] for _ in range(10)]

            # Distribuye según el dígito en la posición actual
            for elemento in lista_normalizada:
                digito = int(elemento[posicion])
                lista_auxiliar[digito].append(elemento)

            # Aplana la lista auxiliar en una sola lista
            lista_normalizada = [
                elemento for sublista in lista_auxiliar for elemento in sublista
            ]

        # Convierte de vuelta a enteros
        self.__lista = [int(elemento) for elemento in lista_normalizada]
        return self.__lista