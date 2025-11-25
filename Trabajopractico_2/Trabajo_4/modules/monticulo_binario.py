# modules/monticulo_binario.py

class MonticuloBinario:
    """
    Implementación de un Montículo Binario Mínimo (Min-Heap) usando una lista.
    El elemento más pequeño siempre queda en la raíz (posición 1).
    """

    def __init__(self):
        """Inicializa un montículo vacío."""
        self.listaMonticulo = [0]  # índice 0 de relleno
        self.tamanoActual = 0

    def infiltArriba(self, i):
        """Mueve el elemento en posición i hacia arriba hasta restaurar el orden."""
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2]:
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = \
                    self.listaMonticulo[i // 2], self.listaMonticulo[i]
            i //= 2

    def insertar(self, k):
        """
        Inserta un nuevo elemento k en el montículo.
        Complejidad: O(log n)
        """
        self.listaMonticulo.append(k)
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def hijoMin(self, i):
        """Devuelve el índice del hijo más chico del nodo en i."""
        if i * 2 + 1 > self.tamanoActual:
            # Solo tiene hijo izquierdo
            return i * 2
        else:
            # Tiene dos hijos, elegimos el menor
            if self.listaMonticulo[i * 2] < self.listaMonticulo[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def infiltAbajo(self, i):
        """Mueve el elemento en posición i hacia abajo hasta restaurar el orden."""
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                self.listaMonticulo[i], self.listaMonticulo[hm] = \
                    self.listaMonticulo[hm], self.listaMonticulo[i]
            i = hm

    def eliminarMin(self):
        """
        Elimina y devuelve el elemento mínimo (raíz).
        Devuelve None si está vacío.
        Complejidad: O(log n)
        """
        if self.tamanoActual == 0:
            return None

        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual -= 1
        self.listaMonticulo.pop()

        if self.tamanoActual > 0:
            self.infiltAbajo(1)

        return valorSacado

    def construirMonticulo(self, unaLista):
        """
        Construye un montículo a partir de una lista.
        Más eficiente que insertar uno a uno. O(n)
        """
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while i > 0:
            self.infiltAbajo(i)
            i -= 1

    def esta_vacio(self):
        """Devuelve True si el montículo está vacío."""
        return self.tamanoActual == 0

    def tamano(self):
        """Devuelve la cantidad de elementos en el montículo."""
        return self.tamanoActual

    def ver_lista_interna(self):
        """Devuelve una copia de la lista interna sin el 0 inicial."""
        return self.listaMonticulo[1:]