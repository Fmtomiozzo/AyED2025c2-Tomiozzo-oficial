# modules/cola_prioridad.py

from modules.monticulo_binario import MonticuloBinario


class ColaPrioridad:
    """
    Cola de Prioridad genérica implementada usando un Montículo Binario Mínimo.

    - Menor prioridad numérica = mayor prioridad lógica.
    - En caso de empate de prioridad, respeta el orden de llegada (FIFO).
    """

    def __init__(self):
        """Inicializa una cola de prioridad vacía."""
        self._monticulo = MonticuloBinario()
        self._contador = 0  # para desempatar por orden de llegada

    def insertar(self, prioridad, dato):
        """
        Inserta un 'dato' con una 'prioridad' (entero).
        Complejidad: O(log n)
        """
        clave_orden = (prioridad, self._contador)
        self._monticulo.insertar((clave_orden, dato))
        self._contador += 1

    def extraer(self):
        """
        Extrae y devuelve el dato con mayor prioridad.
        Devuelve None si está vacía.
        Complejidad: O(log n)
        """
        if self.esta_vacia():
            return None
        clave_orden, dato = self._monticulo.eliminarMin()
        return dato

    def esta_vacia(self):
        """True si no hay elementos en la cola."""
        return self._monticulo.esta_vacio()

    def tamano(self):
        """Cantidad de elementos en la cola."""
        return self._monticulo.tamano()

    def ver_proximo(self):
        """
        Devuelve el dato con mayor prioridad SIN extraerlo.
        Devuelve None si está vacía.
        Complejidad: O(1)
        """
        if self.esta_vacia():
            return None
        clave_orden, dato = self._monticulo.listaMonticulo[1]
        return dato

    def ver_todos(self):
        """
        Devuelve una lista con todos los datos ordenados por prioridad.
        Solo para visualización. No modifica la cola.
        Complejidad: O(n log n) por el sorted.
        """
        elementos_en_monticulo = self._monticulo.ver_lista_interna()
        elementos_ordenados = sorted(elementos_en_monticulo)
        return [dato for clave_orden, dato in elementos_ordenados]