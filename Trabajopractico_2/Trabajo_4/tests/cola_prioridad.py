# -*- coding: utf-8 -*-
"""
Estructura de datos genérica: Cola de Prioridad
Implementada con heap (montículo binario)
"""

import heapq


class ColaPrioridad:
    """
    Cola de prioridad genérica implementada con heap.
    Permite insertar elementos con prioridad y extraer siempre
    el de mayor prioridad (menor valor numérico).
    
    En caso de empate de prioridad, se respeta el orden de llegada.
    """
    
    def __init__(self):
        """Inicializa la cola de prioridad vacía"""
        self._heap = []
        self._contador = 0  # para desempatar por orden de llegada
    
    def insertar(self, prioridad, dato):
        """
        Inserta un elemento con una prioridad dada.
        
        Args:
            prioridad (int): Valor de prioridad (menor = más urgente)
            dato: Cualquier objeto a almacenar
        
        Complejidad: O(log n)
        """
        heapq.heappush(self._heap, (prioridad, self._contador, dato))
        self._contador += 1
    
    def extraer(self):
        """
        Extrae y devuelve el elemento con mayor prioridad.
        
        Returns:
            El dato con mayor prioridad, o None si está vacía
        
        Complejidad: O(log n)
        """
        if self.esta_vacia():
            return None
        return heapq.heappop(self._heap)[2]  # devuelve solo el dato
    
    def esta_vacia(self):
        """
        Verifica si la cola está vacía.
        
        Returns:
            bool: True si está vacía, False en caso contrario
        
        Complejidad: O(1)
        """
        return len(self._heap) == 0
    
    def tamaño(self):
        """
        Devuelve la cantidad de elementos en la cola.
        
        Returns:
            int: Número de elementos
        
        Complejidad: O(1)
        """
        return len(self._heap)
    
    def ver_todos(self):
        """
        Devuelve una lista con todos los elementos ordenados por prioridad.
        Útil solo para visualización, no modifica la cola.
        
        Returns:
            list: Lista de elementos ordenados
        
        Complejidad: O(n log n)
        """
        return [elem[2] for elem in sorted(self._heap)]