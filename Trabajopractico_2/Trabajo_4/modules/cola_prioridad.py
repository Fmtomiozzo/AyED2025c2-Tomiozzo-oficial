# modules/cola_prioridad.py

from modules.monticulo_binario import MonticuloBinario

class ColaPrioridad:
    """
    Cola de Prioridad genérica implementada usando un Montículo Binario Mínimo.

    Características:
    - Almacena elementos con una prioridad asociada.
    - Siempre extrae el elemento con la prioridad más alta (menor valor numérico).
    - Resuelve empates de prioridad usando el orden de llegada (FIFO).
    - Es genérica: puede almacenar cualquier tipo de dato.
    """

    def __init__(self):
        """Inicializa una cola de prioridad vacía."""
        self._monticulo = MonticuloBinario()
        self._contador = 0

    def insertar(self, prioridad, dato):
        """
        Inserta un 'dato' en la cola con su 'prioridad' asociada.
        La prioridad es un número: menor número = mayor prioridad.
        Complejidad: O(log n)
        """
        clave_orden = (prioridad, self._contador)
        self._monticulo.insertar((clave_orden, dato))
        self._contador += 1

    def extraer(self):
        """
        Extrae y devuelve el elemento con mayor prioridad.
        Devuelve None si la cola está vacía.
        Complejidad: O(log n)
        """
        if self.esta_vacia():
            return None
        clave_orden, dato = self._monticulo.eliminarMin()
        return dato

    def esta_vacia(self):
        """Devuelve True si la cola de prioridad no contiene elementos."""
        return self._monticulo.esta_vacio()

    def tamano(self):
        """Devuelve la cantidad de elementos en la cola de prioridad."""
        return self._monticulo.tamano()

    def ver_proximo(self):
        """
        Devuelve el dato con la mayor prioridad SIN eliminarlo de la cola.
        Devuelve None si la cola está vacía.
        Complejidad: O(1)
        """
        if self.esta_vacia():
            return None
        clave_orden, dato = self._monticulo.listaMonticulo[1]
        return dato

    def ver_todos(self):
        """
        Devuelve una lista con todos los datos de la cola, ordenados por prioridad.
        Esta función es solo para visualización y no modifica la cola.
        Complejidad: O(n log n) debido a la ordenación.
        """
        elementos_en_monticulo = self._monticulo.ver_lista_interna()
        elementos_ordenados = sorted(elementos_en_monticulo)
        return [dato for clave_orden, dato in elementos_ordenados]