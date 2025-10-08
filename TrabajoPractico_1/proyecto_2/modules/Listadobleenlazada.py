class Nodo:
    """Nodo para lista doblemente enlazada"""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDobleEnlazada:
    """Implementación de TAD Lista Doblemente Enlazada"""
    
    def __init__(self):
        """Inicializa una lista vacía"""
        self.cabeza = None
        self.cola = None
        self.tamanio = 0
    
    def esta_vacia(self):
        """Devuelve True si la lista está vacía - O(1)"""
        return self.cabeza is None
    
    def agregar_al_inicio(self, item):
        """Agrega un nuevo ítem al inicio de la lista - O(1)"""
        nuevo_nodo = Nodo(item)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        
        self.tamanio += 1
    
    def agregar_al_final(self, item):
        """Agrega un nuevo ítem al final de la lista - O(1)"""
        nuevo_nodo = Nodo(item)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        
        self.tamanio += 1
    
    def _obtener_nodo(self, posicion):
        """Método auxiliar para obtener nodo en posición dada - O(n)"""
        # Manejar índices negativos
        if posicion < 0:
            posicion = self.tamanio + posicion
        
        if posicion < 0 or posicion >= self.tamanio:
            raise IndexError("Posición fuera de rango")
        
        # Optimización: empezar desde el extremo más cercano
        if posicion <= self.tamanio // 2:
            # Empezar desde el inicio
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
        else:
            # Empezar desde el final
            actual = self.cola
            for _ in range(self.tamanio - 1 - posicion):
                actual = actual.anterior
        
        return actual
    
    def insertar(self, item, posicion=None):
        """Agrega un nuevo ítem en la posición especificada"""
        if posicion is None:
            self.agregar_al_final(item)
            return
        
        # Manejar índices negativos
        if posicion < 0:
            posicion = self.tamanio + posicion + 1
        
        if posicion < 0 or posicion > self.tamanio:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            self.agregar_al_inicio(item)
        elif posicion == self.tamanio:
            self.agregar_al_final(item)
        else:
            nuevo_nodo = Nodo(item)
            nodo_actual = self._obtener_nodo(posicion)
            
            nuevo_nodo.siguiente = nodo_actual
            nuevo_nodo.anterior = nodo_actual.anterior
            nodo_actual.anterior.siguiente = nuevo_nodo
            nodo_actual.anterior = nuevo_nodo
            
            self.tamanio += 1
    
    def extraer(self, posicion=None):
        """Elimina y devuelve el ítem en la posición especificada"""
        if self.esta_vacia():
            raise IndexError("No se puede extraer de una lista vacía")
        
        if posicion is None:
            posicion = self.tamanio - 1
        
        # Manejar índices negativos
        if posicion < 0:
            posicion = self.tamanio + posicion
        
        if posicion < 0 or posicion >= self.tamanio:
            raise IndexError("Posición fuera de rango")
        
        # Casos especiales para O(1) en los extremos
        if posicion == 0:
            # Extraer del inicio - O(1)
            dato = self.cabeza.dato
            self.cabeza = self.cabeza.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None
            self.tamanio -= 1
            return dato
        
        elif posicion == self.tamanio - 1:
            # Extraer del final - O(1)
            dato = self.cola.dato
            self.cola = self.cola.anterior
            if self.cola:
                self.cola.siguiente = None
            else:
                self.cabeza = None
            self.tamanio -= 1
            return dato
        
        else:
            # Extraer del medio - O(n)
            nodo_a_extraer = self._obtener_nodo(posicion)
            dato = nodo_a_extraer.dato
            
            nodo_a_extraer.anterior.siguiente = nodo_a_extraer.siguiente
            nodo_a_extraer.siguiente.anterior = nodo_a_extraer.anterior
            
            self.tamanio -= 1
            return dato
    
    def copiar(self):
        """Realiza una copia de la lista - O(n)"""
        nueva_lista = ListaDobleEnlazada()
        actual = self.cabeza
        
        while actual is not None:
            nueva_lista.agregar_al_final(actual.dato)
            actual = actual.siguiente
        
        return nueva_lista
    
    def invertir(self):
        """Invierte el orden de los elementos - O(n)"""
        if self.esta_vacia() or self.tamanio == 1:
            return
        
        actual = self.cabeza
        
        # Intercambiar punteros siguiente y anterior para cada nodo
        while actual is not None:
            # Intercambiar punteros
            actual.siguiente, actual.anterior = actual.anterior, actual.siguiente
            actual = actual.anterior  # Moverse al siguiente (que ahora es anterior)
        
        # Intercambiar cabeza y cola
        self.cabeza, self.cola = self.cola, self.cabeza
    
    def concatenar(self, otra_lista):
        """Concatena otra lista al final de esta - MODIFICA la lista actual"""
        actual = otra_lista.cabeza
        while actual is not None:
            self.agregar_al_final(actual.dato)
            actual = actual.siguiente
    
    def __len__(self):
        """Devuelve el número de ítems - O(1)"""
        return self.tamanio
    
    def __add__(self, otra_lista):
        """Suma dos listas - devuelve nueva lista sin modificar originales"""
        nueva_lista = self.copiar()
        nueva_lista.concatenar(otra_lista)
        return nueva_lista
    
    def __iter__(self):
        """Permite recorrer la lista con for - O(n)"""
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente