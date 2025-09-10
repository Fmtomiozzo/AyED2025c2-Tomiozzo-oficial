# Excepción personalizada para cuando se intenta sacar una carta de un mazo vacío
class DequeEmptyError(Exception):
    """Excepción lanzada cuando se intenta extraer una carta de un mazo vacío"""
    pass


class NodoDoble:
    """
    Nodo para lista doblemente enlazada.
    Cada nodo contiene:
    - dato: la carta que almacena
    - siguiente: referencia al siguiente nodo
    - anterior: referencia al nodo anterior
    """
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class Mazo:
    """
    Implementación de un mazo de cartas usando una lista doblemente enlazada.
    
    Funciona como un deque (double-ended queue) donde:
    - Se puede insertar y extraer tanto del inicio (arriba) como del final (abajo)
    - Mantiene referencias a cabeza y cola para operaciones O(1)
    """
    
    def __init__(self):
        """
        Inicializa un mazo vacío.
        - cabeza: apunta al primer nodo (carta de arriba del mazo)
        - cola: apunta al último nodo (carta de abajo del mazo)  
        - tamaño: contador de cartas en el mazo
        """
        self.cabeza = None
        self.cola = None
        self.tamaño = 0
    
    def poner_carta_arriba(self, carta):
        """
        Inserta una carta en la parte superior del mazo (cabeza de la lista).
        
        Proceso:
        1. Crear nuevo nodo con la carta
        2. Si el mazo está vacío, el nuevo nodo es tanto cabeza como cola
        3. Si no está vacío, insertar al inicio y actualizar enlaces
        
        Args:
            carta: objeto Carta a insertar
        """
        nuevo_nodo = NodoDoble(carta)
        
        if self.cabeza is None:  # Mazo vacío
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:  # Mazo con cartas
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        
        self.tamaño += 1
    
    def poner_carta_abajo(self, carta):
        """
        Inserta una carta en la parte inferior del mazo (cola de la lista).
        
        Proceso:
        1. Crear nuevo nodo con la carta
        2. Si el mazo está vacío, el nuevo nodo es tanto cabeza como cola
        3. Si no está vacío, insertar al final y actualizar enlaces
        
        Args:
            carta: objeto Carta a insertar
        """
        nuevo_nodo = NodoDoble(carta)
        
        if self.cola is None:  # Mazo vacío
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:  # Mazo con cartas
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        
        self.tamaño += 1
    
    def sacar_carta_arriba(self, mostrar=False):
        """
        Extrae la carta de la parte superior del mazo (cabeza de la lista).
        
        Proceso:
        1. Verificar que el mazo no esté vacío (lanzar excepción si lo está)
        2. Guardar la carta a extraer
        3. Actualizar la cabeza al siguiente nodo
        4. Manejar caso especial cuando queda vacío
        5. Opcionalmente hacer visible la carta
        
        Args:
            mostrar (bool): si True, hace visible la carta antes de devolverla
            
        Returns:
            Carta: la carta extraída del tope del mazo
            
        Raises:
            DequeEmptyError: si el mazo está vacío
        """
        if self.cabeza is None:
            raise DequeEmptyError("No se puede sacar una carta de un mazo vacío")
        
        # Guardar la carta que vamos a extraer
        carta_extraida = self.cabeza.dato
        
        # Actualizar la cabeza
        self.cabeza = self.cabeza.siguiente
        
        if self.cabeza is None:  # El mazo quedó vacío
            self.cola = None
        else:  # Aún hay cartas
            self.cabeza.anterior = None
        
        self.tamaño -= 1
        
        # Si se solicita mostrar la carta, hacerla visible
        if mostrar:
            carta_extraida.visible = True
        
        return carta_extraida
    
    def __len__(self):
        """
        Devuelve el número de cartas en el mazo.
        Permite usar len(mazo) en el código.
        
        Returns:
            int: cantidad de cartas en el mazo
        """
        return self.tamaño
    
    def __str__(self):
        """
        Representación en string del mazo.
        Muestra todas las cartas desde la cabeza hasta la cola.
        
        Returns:
            str: representación del mazo como lista de cartas
        """
        if self.cabeza is None:
            return "[]"
        
        cartas = []
        nodo_actual = self.cabeza
        
        # Recorrer desde la cabeza hasta la cola
        while nodo_actual is not None:
            cartas.append(str(nodo_actual.dato))
            nodo_actual = nodo_actual.siguiente
        
        return "[" + ", ".join(cartas) + "]"
    
    def esta_vacio(self):
        """
        Método auxiliar para verificar si el mazo está vacío.
        
        Returns:
            bool: True si el mazo está vacío, False en caso contrario
        """
        return self.cabeza is None


# Código de prueba para verificar que funciona correctamente
if __name__ == "__main__":
    # Importar Carta para las pruebas
    from carta import Carta
    
    print("=== PRUEBAS DEL MAZO ===\n")
    
    # Crear un mazo vacío
    mazo = Mazo()
    print(f"Mazo vacío: {mazo}")
    print(f"Tamaño: {len(mazo)}")
    print(f"¿Está vacío? {mazo.esta_vacio()}\n")
    
    # Crear algunas cartas de prueba
    carta1 = Carta('5', '♣')
    carta2 = Carta('K', '♥')
    carta3 = Carta('A', '♠')
    
    # Hacer visibles las cartas para poder verlas
    carta1.visible = True
    carta2.visible = True
    carta3.visible = True
    
    print("=== PRUEBA: PONER CARTAS ARRIBA ===")
    mazo.poner_carta_arriba(carta1)
    print(f"Después de poner {carta1} arriba: {mazo}")
    
    mazo.poner_carta_arriba(carta2)
    print(f"Después de poner {carta2} arriba: {mazo}")
    
    mazo.poner_carta_arriba(carta3)
    print(f"Después de poner {carta3} arriba: {mazo}")
    print(f"Tamaño del mazo: {len(mazo)}\n")
    
    print("=== PRUEBA: SACAR CARTAS ARRIBA ===")
    carta_sacada = mazo.sacar_carta_arriba()
    print(f"Carta sacada: {carta_sacada}")
    print(f"Mazo después de sacar: {mazo}")
    
    carta_sacada = mazo.sacar_carta_arriba()
    print(f"Carta sacada: {carta_sacada}")
    print(f"Mazo después de sacar: {mazo}")
    print(f"Tamaño del mazo: {len(mazo)}\n")
    
    print("=== PRUEBA: PONER CARTAS ABAJO ===")
    mazo.poner_carta_abajo(carta2)  # Reutilizamos carta2
    print(f"Después de poner {carta2} abajo: {mazo}")
    
    mazo.poner_carta_abajo(carta3)  # Reutilizamos carta3
    print(f"Después de poner {carta3} abajo: {mazo}")
    print(f"Tamaño del mazo: {len(mazo)}\n")
    
    print("=== PRUEBA: VACIAR MAZO ===")
    while len(mazo) > 0:
        carta_sacada = mazo.sacar_carta_arriba()
        print(f"Sacando: {carta_sacada}, quedan {len(mazo)} cartas")
    
    print(f"Mazo final: {mazo}")
    
    print("\n=== PRUEBA: EXCEPCIÓN MAZO VACÍO ===")
    try:
        mazo.sacar_carta_arriba()
    except DequeEmptyError as e:
        print(f"Excepción capturada correctamente: {e}")
    
    print("\n¡Todas las pruebas completadas!")