class Quicksort:
    def __init__(self, lista):
        # Constructor que inicializa el objeto con la lista que se desea ordenar.
        # La lista se almacena como un atributo privado (__lista) del objeto.
        self.__lista = lista

    def ordenar(self, indice_inicio=None, indice_final=None, lista=None):
        # Método que implementa el algoritmo de Quicksort para ordenar la lista.
        # Si no se pasan índices de inicio y final, ni una lista, se usan los valores por defecto.

        if lista is None:
            # Si no se pasa una lista al método, se usa la lista almacenada en el objeto.
            lista = self.__lista

        if indice_inicio is None:
            # Si no se pasa un índice de inicio, se toma el primer elemento de la lista.
            indice_inicio = 0
        if indice_final is None:
            # Si no se pasa un índice final, se toma el último elemento de la lista.
            indice_final = len(lista) - 1

        if indice_inicio < indice_final:
            # Este condicional verifica que aún haya elementos en la sublista que necesitan ser ordenados.
            # Si el índice de inicio es igual o mayor que el índice final, la sublista tiene uno o ningún elemento y no necesita ordenarse.

            # El método __ubicar_pivote posiciona el pivote en su lugar correcto y devuelve su posición.
            posicion_pivote = self.__ubicar_pivote(indice_inicio, indice_final, lista)

            # Se ordena recursivamente la sublista a la izquierda del pivote.
            self.ordenar(indice_inicio, posicion_pivote - 1, lista)

            # Se ordena recursivamente la sublista a la derecha del pivote.
            self.ordenar(posicion_pivote + 1, indice_final, lista)

        # Retorna la lista ordenada después de que toda la recursión ha terminado.
        return self.__lista

    def __ubicar_pivote(self, indice_inicio=None, indice_final=None, lista=None):
        # Método privado que posiciona correctamente el pivote en la lista.
        # Todos los elementos menores que el pivote se moverán a la izquierda de éste,
        # y todos los elementos mayores que el pivote se moverán a la derecha.

        pivote = lista[indice_inicio]  # Se toma como pivote el primer elemento de la sublista.
        izquierda = indice_inicio + 1  # El índice izquierdo comienza justo después del pivote.
        derecha = indice_final  # El índice derecho comienza en el último elemento de la sublista.

        while True:
            # Bucle infinito que continúa hasta que los índices izquierda y derecha se cruzan. Es decir que el indice izquierdo es mayor que el derecho
            # Esto significa que hemos terminado de dividir la sublista en dos partes: 
            # una con elementos menores o iguales al pivote y otra con elementos mayores.

            # Mover el índice izquierda hacia la derecha hasta encontrar un elemento mayor que el pivote.
            # Chequear izqierda,  es decir ahora recorremos de izquierda a derecha
            while izquierda <= derecha and lista[izquierda] <= pivote:
                izquierda += 1  # Avanza el índice izquierdo hacia la derecha.

            # Mover el índice derecha hacia la izquierda hasta encontrar un elemento menor que el pivote.
            # Chequear derecha, es decir, de derecha a izquierda recorremos la lista
            while izquierda <= derecha and lista[derecha] >= pivote:
                derecha -= 1  # Retrocede el índice derecho hacia la izquierda.

            if izquierda <= derecha:
                # Si los índices izquierda y derecha aún no se han cruzado, significa que:
                # - Hay un elemento en la posición izquierda que debería estar a la derecha del pivote.
                # - Hay un elemento en la posición derecha que debería estar a la izquierda del pivote.
                # Se intercambian estos elementos para continuar dividiendo la sublista en dos partes correctas.
                lista[izquierda], lista[derecha] = lista[derecha], lista[izquierda]
            else:
                # Si los índices se han cruzado (izquierda > derecha), significa que todos los elementos a la izquierda del índice derecha
                # son menores o iguales al pivote y todos los elementos a la derecha del índice izquierda son mayores que el pivote.
                # En este punto, el bucle termina porque la sublista está correctamente dividida.
                break

        # Después de dividir la sublista, colocamos el pivote en su posición correcta:
        # intercambiamos el pivote (que estaba al principio) con el elemento en la posición derecha.
        #Intercambiar con izquierda no sería correcto porque izquierda ya ha avanzado más allá de los elementos menores o iguales al pivote.
        lista[indice_inicio], lista[derecha] = lista[derecha], lista[indice_inicio]

        # Retorna la posición final del pivote, que ahora está correctamente colocado.
        return derecha

    def __str__(self):
        # Método especial que devuelve la lista como una cadena cuando se llama a print() sobre el objeto.
        return f"{self.__lista}"
    


"""Ejemplo:
Veamos cómo funciona con la lista [5, 4, 8, 9]:

Estado inicial:
Lista: [5, 4, 8, 9]
Pivote: 5 (el primer elemento)
Índice izquierda: 1 (elemento 4)
Índice derecha: 3 (elemento 9)

Primer bucle while (comenza desde la izquierda):
Objetivo: Avanzar izquierda, es decir el indce, mientras los elementos sean menores o iguales al pivote.
Comienza en el índice 1 con el elemento 4.
4 <= 5 (cierto), entonces izquierda avanza al índice 2 (elemento 8).
8 <= 5 (falso), el bucle izquierda se detiene. Aca el valor de izquuierda es = 2

Segundo bucle while (comienza desde la derecha):
Objetivo: Retroceder derecha, es decir avanzar hacia la izquierda cambiando el indice derecha mientras los elementos sean mayores o iguales al pivote.
Comienza en el índice 3 con el elemento 9.
9 >= 5 (cierto), entonces derecha retrocede al índice 2 (elemento 8).
8 >= 5 (cierto), entonces derecha retrocede al índice 1 (elemento 4).
4 >= 5 (falso), el bucle derecha se detiene. Acá el valor de izquierda es = 1

Estado después de ambos bucles:
Índice izquierda: 2 (elemento 8)
Índice derecha: 1 (elemento 4)

Evaluación del if:
Condición: izquierda <= derecha (2 <= 1), lo cual es falso.
Resultado: No se realiza ningún intercambio, y el bucle principal while se detiene.

Finalización:
Se intercambia el pivote con el elemento en el índice derecha.
La lista se convierte en [4, 5, 8, 9].
El pivote 5 ahora está en su posición correcta, y el proceso de ordenación continúa recursivamente en las sublistas [4] y [8, 9]."""