from datetime import datetime
from typing import Optional, Tuple, List
import os

from .AVL import ArbolAVL, NodoAVL   # usa el AVL genérico


class Temperaturas_DB:
    def __init__(self):
        self._arbol = ArbolAVL()     # AVL interno

    # ---- conversión fechas ----

    def _to_dt(self, s: str) -> datetime:
        # limpia espacios y posible BOM al inicio (por si el archivo es UTF-16 LE)
        s = s.strip().lstrip('\ufeff')
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        raise ValueError(f"Formato de fecha inválido: {s!r}")

    def _to_str(self, d: datetime) -> str:
        return d.strftime("%d/%m/%Y")

    # ---- API pública ----

    def guardar_temperatura(self, temperatura: float, fecha: str):
        f = self._to_dt(fecha)
        self._arbol.insertar(f, temperatura)

    def devolver_temperatura(self, fecha: str) -> Optional[float]:
        f = self._to_dt(fecha)
        return self._arbol.buscar(f)

    def borrar_temperatura(self, fecha: str) -> bool:
        f = self._to_dt(fecha)
        return self._arbol.eliminar(f)

    def cantidad_muestras(self) -> int:
        return self._arbol.cantidad_nodos()

    # ---- operaciones sobre rangos ----

    def max_temp_rango(self, f1: str, f2: str) -> Optional[float]:
        return self._max_r(self._arbol.raiz, self._to_dt(f1), self._to_dt(f2))

    def _max_r(self, n: Optional[NodoAVL], a: datetime, b: datetime) -> Optional[float]:
        if not n:
            return None
        if n.clave < a:
            return self._max_r(n.der, a, b)
        if n.clave > b:
            return self._max_r(n.izq, a, b)

        m = n.valor
        izq = self._max_r(n.izq, a, b)
        der = self._max_r(n.der, a, b)
        if izq is not None:
            m = max(m, izq)
        if der is not None:
            m = max(m, der)
        return m

    def min_temp_rango(self, f1: str, f2: str) -> Optional[float]:
        return self._min_r(self._arbol.raiz, self._to_dt(f1), self._to_dt(f2))

    def _min_r(self, n: Optional[NodoAVL], a: datetime, b: datetime) -> Optional[float]:
        if not n:
            return None
        if n.clave < a:
            return self._min_r(n.der, a, b)
        if n.clave > b:
            return self._min_r(n.izq, a, b)

        m = n.valor
        izq = self._min_r(n.izq, a, b)
        der = self._min_r(n.der, a, b)
        if izq is not None:
            m = min(m, izq)
        if der is not None:
            m = min(m, der)
        return m

    def temp_extremos_rango(self, f1: str, f2: str) -> Tuple[Optional[float], Optional[float]]:
        return self.min_temp_rango(f1, f2), self.max_temp_rango(f1, f2)

    def devolver_temperaturas(self, f1: str, f2: str) -> List[str]:
        a, b = self._to_dt(f1), self._to_dt(f2)
        res: List[str] = []
        self._inorden_r(self._arbol.raiz, a, b, res)
        return res

    def _inorden_r(self, n: Optional[NodoAVL], a: datetime, b: datetime, out: List[str]):
        if not n:
            return
        if n.clave > a:
            self._inorden_r(n.izq, a, b, out)
        if a <= n.clave <= b:
            out.append(f"{self._to_str(n.clave)}: {n.valor} ºC")
        if n.clave < b:
            self._inorden_r(n.der, a, b, out)

    # ---- carga desde archivo ----

    def cargar_desde_archivo(self) -> Tuple[int, int]:
        ruta = os.path.join(os.path.dirname(__file__), "muestras.txt")
        lp = rc = 0
        # el archivo está en UTF‑16 LE, por eso usamos ese encoding
        with open(ruta, "r", encoding="utf-16-le") as f:
            for linea in f:
                s = linea.strip()
                if not s:
                    continue

                # limpia posible BOM al inicio de la primera línea
                s = s.lstrip('\ufeff')

                partes = s.split(';') if ';' in s else (s.split(',') if ',' in s else [])
                if len(partes) != 2:
                    continue

                fecha_str = partes[0].strip()
                temp = float(partes[1].strip())
                self.guardar_temperatura(temp, fecha_str)
                lp += 1
                rc += 1
        return lp, rc