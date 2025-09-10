import time
import matplotlib.pyplot as plt
import numpy as np

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

def medir_tiempo_len(lista):
    """Mide el tiempo de ejecución del método len"""
    inicio = time.perf_counter()
    len(lista)
    fin = time.perf_counter()
    return fin - inicio

def medir_tiempo_copiar(lista):
    """Mide el tiempo de ejecución del método copiar"""
    inicio = time.perf_counter()
    lista.copiar()
    fin = time.perf_counter()
    return fin - inicio

def medir_tiempo_invertir(lista):
    """Mide el tiempo de ejecución del método invertir"""
    # Crear una copia para no modificar la original
    lista_copia = lista.copiar()
    inicio = time.perf_counter()
    lista_copia.invertir()
    fin = time.perf_counter()
    return fin - inicio

def crear_lista_con_n_elementos(n):
    """Crea una lista con n elementos"""
    lista = ListaDobleEnlazada()
    for i in range(n):
        lista.agregar_al_final(i)
    return lista

def realizar_mediciones():
    """Realiza las mediciones de rendimiento"""
    # Tamaños de lista a probar
    tamanios = [100, 500, 1000, 2000, 3000, 4000, 5000, 7500, 10000, 15000]
    
    tiempos_len = []
    tiempos_copiar = []
    tiempos_invertir = []
    
    print("Realizando mediciones...")
    
    for n in tamanios:
        print(f"Midiendo para n = {n}")
        
        # Crear lista con n elementos
        lista = crear_lista_con_n_elementos(n)
        
        # Medir len (promedio de múltiples ejecuciones para mayor precisión)
        tiempos_len_temp = []
        for _ in range(1000):  # Muchas repeticiones porque len es muy rápido
            tiempos_len_temp.append(medir_tiempo_len(lista))
        tiempos_len.append(np.mean(tiempos_len_temp))
        
        # Medir copiar (promedio de múltiples ejecuciones)
        tiempos_copiar_temp = []
        for _ in range(10):
            tiempos_copiar_temp.append(medir_tiempo_copiar(lista))
        tiempos_copiar.append(np.mean(tiempos_copiar_temp))
        
        # Medir invertir (promedio de múltiples ejecuciones)
        tiempos_invertir_temp = []
        for _ in range(10):
            tiempos_invertir_temp.append(medir_tiempo_invertir(lista))
        tiempos_invertir.append(np.mean(tiempos_invertir_temp))
    
    return tamanios, tiempos_len, tiempos_copiar, tiempos_invertir

# Realizar las mediciones
tamanios, tiempos_len, tiempos_copiar, tiempos_invertir = realizar_mediciones()

# ================================
# Gráfica 1: len() en MICROSEGUNDOS
# ================================
plt.figure(figsize=(8, 5))
plt.plot(tamanios, [t*1e6 for t in tiempos_len], 'bo-', linewidth=2, markersize=6)
plt.title('Método len() - O(1)', fontsize=12, fontweight='bold')
plt.xlabel('Número de elementos (N)')
plt.ylabel('Tiempo (microsegundos)')
plt.grid(True, alpha=0.3)
plt.show()

# ================================
# Gráficas individuales en SEGUNDOS
# ================================
plt.figure(figsize=(15, 5))

# len
plt.subplot(1, 3, 1)
plt.plot(tamanios, tiempos_len, 'bo-', linewidth=2, markersize=6)
plt.title('Método len() - O(1)', fontsize=12, fontweight='bold')
plt.xlabel('Número de elementos (N)')
plt.ylabel('Tiempo (segundos)')
plt.grid(True, alpha=0.3)

# copiar
plt.subplot(1, 3, 2)
plt.plot(tamanios, tiempos_copiar, 'ro-', linewidth=2, markersize=6)
plt.title('Método copiar() - O(n)', fontsize=12, fontweight='bold')
plt.xlabel('Número de elementos (N)')
plt.ylabel('Tiempo (segundos)')
plt.grid(True, alpha=0.3)

# invertir
plt.subplot(1, 3, 3)
plt.plot(tamanios, tiempos_invertir, 'go-', linewidth=2, markersize=6)
plt.title('Método invertir() - O(n)', fontsize=12, fontweight='bold')
plt.xlabel('Número de elementos (N)')
plt.ylabel('Tiempo (segundos)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ================================
# Comparativa en SEGUNDOS
# ================================
plt.figure(figsize=(12, 8))
plt.plot(tamanios, tiempos_len, 'bo-', label='len() - O(1)', linewidth=2, markersize=6)
plt.plot(tamanios, tiempos_copiar, 'ro-', label='copiar() - O(n)', linewidth=2, markersize=6)
plt.plot(tamanios, tiempos_invertir, 'go-', label='invertir() - O(n)', linewidth=2, markersize=6)

plt.title('Comparación de Complejidades Temporales\nLista Doblemente Enlazada', fontsize=14, fontweight='bold')
plt.xlabel('Número de elementos (N)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.show()

# ================================
# Valores en tabla
# ================================
print("\n=== ANÁLISIS DE RESULTADOS ===")
print(f"Tamaños probados: {tamanios}")
print(f"\nTiempos len() (microsegundos): {[f'{t*1e6:.2f}' for t in tiempos_len]}")
print(f"Tiempos len() (segundos): {[f'{t:.8f}' for t in tiempos_len]}")
print(f"Tiempos copiar() (segundos): {[f'{t:.6f}' for t in tiempos_copiar]}")
print(f"Tiempos invertir() (segundos): {[f'{t:.6f}' for t in tiempos_invertir]}")