from modules.Listadobleenlazada import ListaDobleEnlazada

class DequeEmptyError(Exception):
    """Se lanza al intentar extraer de un mazo vacío."""
    pass

class Mazo:
    def __init__(self):
        self._lista = ListaDobleEnlazada()

    def poner_carta_arriba(self, carta):
        """Coloca una carta en la parte superior (frente) del mazo."""
        self._lista.agregar_al_inicio(carta)

    def poner_carta_abajo(self, carta):
        """Coloca una carta en la parte inferior (final) del mazo."""
        self._lista.agregar_al_final(carta)

    def sacar_carta_arriba(self, mostrar=False):
        """Extrae y devuelve la carta superior. Si mostrar=True, marca visible si existe."""
        if len(self._lista) == 0:
            raise DequeEmptyError("No se puede sacar una carta de un mazo vacío")
        carta = self._lista.extraer(0)
        if mostrar:
            try:
                carta.visible = True
            except AttributeError:
                pass
        return carta

    def __len__(self):
        return len(self._lista)

    def __str__(self):
        return "[" + ", ".join(str(c) for c in self._lista) + "]" if len(self) else "[]"

    def esta_vacio(self):
        return len(self._lista) == 0