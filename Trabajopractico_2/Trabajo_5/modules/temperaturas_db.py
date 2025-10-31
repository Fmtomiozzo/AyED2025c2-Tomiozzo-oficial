from datetime import datetime
from typing import Optional, Tuple, List
import os

class NodoAVL:
    def __init__(self, fecha: datetime, temperatura: float):
        self.fecha = fecha                          # Clave del nodo (fecha)
        self.temperatura = temperatura              # Valor almacenado (temperatura)
        self.altura = 1                             # Altura del nodo para balanceo
        self.izq: Optional['NodoAVL'] = None       # Hijo izquierdo
        self.der: Optional['NodoAVL'] = None       # Hijo derecho

class Temperaturas_DB:
    def __init__(self):
        self.raiz: Optional[NodoAVL] = None        # Raíz del árbol AVL
        self.cantidad = 0                           # Contador de nodos

    # Utilidades
    def _to_dt(self, s: str) -> datetime:          # Convierte string a datetime
        try:
            return datetime.strptime(s, "%d/%m/%Y")
        except:
            return datetime.strptime(s, "%Y-%m-%d")

    def _to_str(self, d: datetime) -> str:         # Convierte datetime a string
        return d.strftime("%d/%m/%Y")

    def _h(self, n: Optional[NodoAVL]) -> int:     # Retorna altura del nodo (0 si es None)
        return n.altura if n else 0

    def _upd(self, n: NodoAVL):                    # Actualiza altura del nodo
        n.altura = 1 + max(self._h(n.izq), self._h(n.der))

    def _bal(self, n: NodoAVL) -> int:             # Calcula factor de balance (izq - der)
        return self._h(n.izq) - self._h(n.der)

    def _rot_der(self, y: NodoAVL) -> NodoAVL:     # Rotación simple derecha
        x = y.izq
        T2 = x.der
        x.der = y
        y.izq = T2
        self._upd(y); self._upd(x)
        return x

    def _rot_izq(self, x: NodoAVL) -> NodoAVL:     # Rotación simple izquierda
        y = x.der
        T2 = y.izq
        y.izq = x
        x.der = T2
        self._upd(x); self._upd(y)
        return y

    # Operaciones principales
    def guardar_temperatura(self, temperatura: float, fecha: str):  # Inserta temperatura (API pública)
        self.raiz = self._ins(self.raiz, self._to_dt(fecha), temperatura)

    def _ins(self, n: Optional[NodoAVL], f: datetime, t: float) -> NodoAVL:  # Inserción recursiva con balanceo AVL
        if not n:                                   # Caso base: crear nuevo nodo
            self.cantidad += 1
            return NodoAVL(f, t)
        if f < n.fecha:                             # Insertar en subárbol izquierdo
            n.izq = self._ins(n.izq, f, t)
        elif f > n.fecha:                           # Insertar en subárbol derecho
            n.der = self._ins(n.der, f, t)
        else:                                       # Fecha existe: actualizar temperatura
            n.temperatura = t
            return n
        self._upd(n)                                # Actualizar altura
        assert n is not None                        # pista para el analizador (evita subrayado rojo)
        b = self._bal(n)                            # Calcular balance
        if b > 1 and f < n.izq.fecha:              # Caso Izquierda-Izquierda
            return self._rot_der(n)
        if b < -1 and f > n.der.fecha:             # Caso Derecha-Derecha
            return self._rot_izq(n)
        if b > 1 and f > n.izq.fecha:              # Caso Izquierda-Derecha
            n.izq = self._rot_izq(n.izq)
            return self._rot_der(n)
        if b < -1 and f < n.der.fecha:             # Caso Derecha-Izquierda
            n.der = self._rot_der(n.der)
            return self._rot_izq(n)
        return n

    def devolver_temperatura(self, fecha: str) -> Optional[float]:  # Busca temperatura por fecha
        n = self._busc(self.raiz, self._to_dt(fecha))
        return n.temperatura if n else None

    def _busc(self, n: Optional[NodoAVL], f: datetime) -> Optional[NodoAVL]:  # Búsqueda binaria recursiva
        if not n or n.fecha == f:                   # Caso base: encontrado o no existe
            return n
        return self._busc(n.izq, f) if f < n.fecha else self._busc(n.der, f)

    def max_temp_rango(self, f1: str, f2: str) -> Optional[float]:  # Temperatura máxima en rango
        return self._max_r(self.raiz, self._to_dt(f1), self._to_dt(f2))

    def _max_r(self, n: Optional[NodoAVL], a: datetime, b: datetime) -> Optional[float]:  # Búsqueda recursiva de máximo
        if not n: return None
        if n.fecha < a: return self._max_r(n.der, a, b)  # Buscar solo a la derecha
        if n.fecha > b: return self._max_r(n.izq, a, b)  # Buscar solo a la izquierda
        m = n.temperatura                           # Nodo actual está en rango
        izq = self._max_r(n.izq, a, b)             # Buscar en ambos subárboles
        der = self._max_r(n.der, a, b)
        if izq is not None: m = max(m, izq)        # Comparar con resultados
        if der is not None: m = max(m, der)
        return m

    def min_temp_rango(self, f1: str, f2: str) -> Optional[float]:  # Temperatura mínima en rango
        return self._min_r(self.raiz, self._to_dt(f1), self._to_dt(f2))

    def _min_r(self, n: Optional[NodoAVL], a: datetime, b: datetime) -> Optional[float]:  # Búsqueda recursiva de mínimo
        if not n: return None
        if n.fecha < a: return self._min_r(n.der, a, b)
        if n.fecha > b: return self._min_r(n.izq, a, b)
        m = n.temperatura
        izq = self._min_r(n.izq, a, b)
        der = self._min_r(n.der, a, b)
        if izq is not None: m = min(m, izq)
        if der is not None: m = min(m, der)
        return m

    def temp_extremos_rango(self, f1: str, f2: str) -> Tuple[Optional[float], Optional[float]]:  # Retorna (min, max) en rango
        return self.min_temp_rango(f1, f2), self.max_temp_rango(f1, f2)

    def borrar_temperatura(self, fecha: str) -> bool:  # Elimina nodo por fecha
        antes = self.cantidad
        self.raiz = self._del(self.raiz, self._to_dt(fecha))
        return self.cantidad < antes                # True si se eliminó algo

    def _del(self, n: Optional[NodoAVL], f: datetime) -> Optional[NodoAVL]:  # Eliminación recursiva con balanceo
        if not n: return None
        if f < n.fecha:                             # Buscar en subárbol izquierdo
            n.izq = self._del(n.izq, f)
        elif f > n.fecha:                           # Buscar en subárbol derecho
            n.der = self._del(n.der, f)
        else:                                       # Nodo encontrado
            if not n.izq and not n.der:            # Caso 1: sin hijos
                self.cantidad -= 1
                return None
            if not n.izq:                          # Caso 2: solo hijo derecho
                self.cantidad -= 1
                return n.der
            if not n.der:                          # Caso 2: solo hijo izquierdo
                self.cantidad -= 1
                return n.izq
            s = self._min_n(n.der)                 # Caso 3: dos hijos (sucesor inorden)
            n.fecha, n.temperatura = s.fecha, s.temperatura
            n.der = self._del(n.der, s.fecha)
        if not n: return None
        assert n is not None                        # pista para el analizador (evita subrayado rojo)
        self._upd(n)                                # Actualizar altura
        b = self._bal(n)                            # Rebalancear (4 casos)
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

    def _min_n(self, n: NodoAVL) -> NodoAVL:       # Encuentra nodo con fecha mínima (más a la izquierda)
        while n.izq: n = n.izq
        return n

    def devolver_temperaturas(self, f1: str, f2: str) -> List[str]:  # Lista temperaturas en rango
        a, b = self._to_dt(f1), self._to_dt(f2)
        res: List[str] = []
        self._inorden_r(self.raiz, a, b, res)
        return res

    def _inorden_r(self, n: Optional[NodoAVL], a: datetime, b: datetime, out: List[str]):  # Recorrido inorden en rango
        if not n: return
        if n.fecha > a: self._inorden_r(n.izq, a, b, out)  # Visitar izquierda si puede haber nodos en rango
        if a <= n.fecha <= b: out.append(f"{self._to_str(n.fecha)}: {n.temperatura} ºC")  # Procesar nodo actual
        if n.fecha < b: self._inorden_r(n.der, a, b, out)  # Visitar derecha si puede haber nodos en rango

    def cantidad_muestras(self) -> int:            # Retorna cantidad total de nodos
        return self.cantidad

    def cargar_desde_archivo(self) -> Tuple[int, int]:  # Carga datos desde muestras.txt
        ruta = os.path.join(os.path.dirname(__file__), "muestras.txt")
        lp = rc = 0                                 # Contadores: líneas procesadas, registros cargados
        with open(ruta, "r", encoding="utf-16-le") as f:
            for linea in f:
                s = linea.strip()
                if not s: continue                  # Saltar líneas vacías
                partes = s.split(';') if ';' in s else (s.split(',') if ',' in s else [])  # Separar por ; o ,
                if len(partes) != 2: continue       # Validar formato
                fecha_str = partes[0].strip()
                temp = float(partes[1].strip())
                self.guardar_temperatura(temp, fecha_str)
                lp += 1; rc += 1
        return lp, rc                               # Retorna (líneas procesadas, registros cargados)