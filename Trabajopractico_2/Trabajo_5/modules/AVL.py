# modules/avl.py
from typing import Optional, Any

class NodoAVL:
    def __init__(self, clave: Any, valor: Any):
        self.clave = clave
        self.valor = valor
        self.altura = 1
        self.izq: Optional['NodoAVL'] = None
        self.der: Optional['NodoAVL'] = None


class ArbolAVL:
    def __init__(self):
        self.raiz: Optional[NodoAVL] = None
        self.cantidad: int = 0

    # utilidades internas
    def _h(self, n: Optional[NodoAVL]) -> int:
        return n.altura if n else 0

    def _upd(self, n: NodoAVL):
        n.altura = 1 + max(self._h(n.izq), self._h(n.der))

    def _bal(self, n: NodoAVL) -> int:
        return self._h(n.izq) - self._h(n.der)

    def _rot_der(self, y: NodoAVL) -> NodoAVL:
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self._upd(y)
        self._upd(x)
        return x

    def _rot_izq(self, x: NodoAVL) -> NodoAVL:
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self._upd(x)
        self._upd(y)
        return y

    # ---- operaciones públicas básicas ----

    def insertar(self, clave, valor):
        self.raiz = self._ins(self.raiz, clave, valor)

    def _ins(self, n: Optional[NodoAVL], c, v) -> NodoAVL:
        if not n:
            self.cantidad += 1
            return NodoAVL(c, v)

        if c < n.clave:
            n.izq = self._ins(n.izq, c, v)
        elif c > n.clave:
            n.der = self._ins(n.der, c, v)
        else:
            # clave existente: actualizar valor
            n.valor = v
            return n

        self._upd(n)
        b = self._bal(n)

        # Casos de rotación
        if b > 1 and c < n.izq.clave:
            return self._rot_der(n)
        if b < -1 and c > n.der.clave:
            return self._rot_izq(n)
        if b > 1 and c > n.izq.clave:
            n.izq = self._rot_izq(n.izq)
            return self._rot_der(n)
        if b < -1 and c < n.der.clave:
            n.der = self._rot_der(n.der)
            return self._rot_izq(n)

        return n

    def buscar(self, clave):
        n = self._busc(self.raiz, clave)
        return n.valor if n else None

    def _busc(self, n: Optional[NodoAVL], c) -> Optional[NodoAVL]:
        if not n or n.clave == c:
            return n
        return self._busc(n.izq, c) if c < n.clave else self._busc(n.der, c)

    def eliminar(self, clave) -> bool:
        antes = self.cantidad
        self.raiz = self._del(self.raiz, clave)
        return self.cantidad < antes

    def _del(self, n: Optional[NodoAVL], c) -> Optional[NodoAVL]:
        if not n:
            return None

        if c < n.clave:
            n.izq = self._del(n.izq, c)
        elif c > n.clave:
            n.der = self._del(n.der, c)
        else:
            # nodo encontrado
            if not n.izq and not n.der:
                self.cantidad -= 1
                return None
            if not n.izq:
                self.cantidad -= 1
                return n.der
            if not n.der:
                self.cantidad -= 1
                return n.izq

            # dos hijos: sucesor inorden
            s = self._min_n(n.der)
            n.clave, n.valor = s.clave, s.valor
            n.der = self._del(n.der, s.clave)

        if not n:
            return None

        self._upd(n)
        b = self._bal(n)

        if b > 1 and self._bal(n.izq) >= 0:
            return self._rot_der(n)
        if b > 1 and self._bal(n.izq) < 0:
            n.izq = self._rot_izq(n.izq)
            return self._rot_der(n)
        if b < -1 and self._bal(n.der) <= 0:
            return self._rot_izq(n)
        if b < -1 and self._bal(n.der) > 0:
            n.der = self._rot_der(n.der)
            return self._rot_izq(n)

        return n

    def _min_n(self, n: NodoAVL) -> NodoAVL:
        while n.izq:
            n = n.izq
        return n

    def cantidad_nodos(self) -> int:
        return self.cantidad