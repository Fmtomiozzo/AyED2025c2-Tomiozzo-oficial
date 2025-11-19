# modules/monticulo_binario.py

class MonticuloBinario:
    """
    Implementación de un Montículo Binario Mínimo (Min-Heap) usando una lista.
    Sigue la lógica de Runestone Academy para la implementación manual.

    Propiedades clave:
    1. Estructura: Es un árbol binario completo, representado eficientemente por una lista.
       - El elemento en listaMonticulo[0] es un valor de relleno (no se usa).
       - El hijo izquierdo de un nodo en posición 'i' está en '2*i'.
       - El hijo derecho de un nodo en posición 'i' está en '2*i + 1'.
       - El padre de un nodo en posición 'i' está en 'i // 2'.
    2. Orden: Para cada nodo 'N' con padre 'P', la clave de 'N' es mayor o igual
       a la clave de 'P'. Esto asegura que el elemento más pequeño siempre está en la raíz.
    """

    def __init__(self):
        """Inicializa un montículo vacío."""
        self.listaMonticulo = [0]
        self.tamanoActual = 0

    def infiltArriba(self, i):
        """
        Mueve el elemento en la posición 'i' hacia arriba en el montículo
        hasta que se restaure la propiedad de orden del montículo.
        Se usa después de insertar un nuevo elemento al final.
        """
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2]:
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = \
                    self.listaMonticulo[i // 2], self.listaMonticulo[i]
            i //= 2

    def insertar(self, k):
        """
        Inserta un nuevo elemento 'k' en el montículo.
        Primero lo añade al final de la lista y luego lo "infiltra" hacia arriba.
        Complejidad: O(log n)
        """
        self.listaMonticulo.append(k)
        self.tamanoActual += 1
        self.infiltArriba(self.tamanoActual)

    def hijoMin(self, i):
        """
        Encuentra y devuelve el índice del hijo con el valor más pequeño
        para el nodo en la posición 'i'.
        """
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i * 2] < self.listaMonticulo[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def infiltAbajo(self, i):
        """
        Mueve el elemento en la posición 'i' hacia abajo en el montículo
        hasta que se restaure la propiedad de orden del montículo.
        Se usa después de reemplazar la raíz con el último elemento.
        """
        while (i * 2) <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                self.listaMonticulo[i], self.listaMonticulo[hm] = \
                    self.listaMonticulo[hm], self.listaMonticulo[i]
            i = hm

    def eliminarMin(self):
        """
        Elimina y devuelve el elemento más pequeño (la raíz) del montículo.
        Para mantener la propiedad de estructura, el último elemento se mueve a la raíz,
        y luego se "infiltra" hacia abajo.
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
        Construye un montículo a partir de una lista de elementos.
        Es más eficiente que insertar uno por uno.
        Complejidad: O(n)
        """
        i = len(unaLista) // 2
        self.tamanoActual = len(unaLista)
        self.listaMonticulo = [0] + unaLista[:]
        while i > 0:
            self.infiltAbajo(i)
            i -= 1

    def esta_vacio(self):
        """Devuelve True si el montículo no contiene elementos."""
        return self.tamanoActual == 0

    def tamano(self):
        """Devuelve la cantidad de elementos en el montículo."""
        return self.tamanoActual

    def ver_lista_interna(self):
        """
        Devuelve una copia de la lista interna del montículo (sin el 0 inicial).
        Útil para depuración o visualización.
        """
        return self.listaMonticulo[1:]