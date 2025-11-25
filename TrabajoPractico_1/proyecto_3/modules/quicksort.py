class Quicksort:
    def __init__(self, lista):
        # La lista se almacena como un atributo privado (__lista) del objeto.
        self.__lista = lista

    def ordenar(self, indice_inicio=None, indice_final=None, lista=None):
        """
        Implementa el algoritmo de Quicksort para ordenar la lista.
        Si no se pasan índices ni lista, usa los valores por defecto del objeto.
        """
        if lista is None:
            lista = self.__lista

        if indice_inicio is None:
            indice_inicio = 0
        if indice_final is None:
            indice_final = len(lista) - 1

        if indice_inicio < indice_final:
            # Ubica el pivote en su posición correcta
            posicion_pivote = self.__ubicar_pivote(indice_inicio, indice_final, lista)

            # Ordena recursivamente las sublistas izquierda y derecha
            self.ordenar(indice_inicio, posicion_pivote - 1, lista)
            self.ordenar(posicion_pivote + 1, indice_final, lista)

        return self.__lista

    def __ubicar_pivote(self, indice_inicio, indice_final, lista):
        """
        Posiciona correctamente el pivote en la lista.
        Todos los elementos menores que el pivote quedan a la izquierda
        y los mayores a la derecha.
        """
        pivote = lista[indice_inicio]
        izquierda = indice_inicio + 1
        derecha = indice_final

        while True:
            # Recorremos desde la izquierda hasta encontrar algo > pivote
            while izquierda <= derecha and lista[izquierda] <= pivote:
                izquierda += 1

            # Recorremos desde la derecha hasta encontrar algo < pivote
            while izquierda <= derecha and lista[derecha] >= pivote:
                derecha -= 1

            if izquierda <= derecha:
                # Intercambiamos los elementos fuera de lugar
                lista[izquierda], lista[derecha] = lista[derecha], lista[izquierda]
            else:
                break

        # Colocamos el pivote en su posición final
        lista[indice_inicio], lista[derecha] = lista[derecha], lista[indice_inicio]
        return derecha

    def __str__(self):
        return f"{self.__lista}"