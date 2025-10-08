"""
Temperaturas_DB - Base de datos de temperaturas con Árbol AVL
Autor: Kevin Kelvin
Descripción: Implementación de una base de datos en memoria usando árbol AVL
             para almacenar y consultar mediciones de temperatura por fecha.
"""

from datetime import datetime
from typing import Optional, Tuple, List


class NodoAVL:
    """Nodo del árbol AVL que almacena una medición de temperatura"""
    
    def __init__(self, fecha: datetime, temperatura: float):
        self.fecha = fecha
        self.temperatura = temperatura
        self.altura = 1
        self.min_temp = temperatura
        self.max_temp = temperatura
        self.izquierdo: Optional['NodoAVL'] = None
        self.derecho: Optional['NodoAVL'] = None


class Temperaturas_DB:
    """
    Base de datos de temperaturas implementada con árbol AVL.
    Permite operaciones eficientes de inserción, búsqueda y consultas por rango.
    """
    
    def __init__(self):
        self.raiz: Optional[NodoAVL] = None
        self.cantidad = 0
    
    # ============ UTILIDADES ============
    
    def _str_a_fecha(self, fecha_str: str) -> datetime:
        """Convierte string dd/mm/aaaa a datetime"""
        return datetime.strptime(fecha_str, "%d/%m/%Y")
    
    def _fecha_a_str(self, fecha: datetime) -> str:
        """Convierte datetime a string dd/mm/aaaa"""
        return fecha.strftime("%d/%m/%Y")
    
    def _altura(self, nodo: Optional[NodoAVL]) -> int:
        """Retorna la altura del nodo"""
        return nodo.altura if nodo else 0
    
    def _balance(self, nodo: Optional[NodoAVL]) -> int:
        """Calcula el factor de balance del nodo"""
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho) if nodo else 0
    
    def _actualizar_altura(self, nodo: NodoAVL):
        """Actualiza la altura del nodo basándose en sus hijos"""
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def _actualizar_extremos(self, nodo: NodoAVL):
        """Actualiza min_temp y max_temp del nodo basado en sus hijos"""
        nodo.min_temp = nodo.temperatura
        nodo.max_temp = nodo.temperatura
        
        if nodo.izquierdo:
            nodo.min_temp = min(nodo.min_temp, nodo.izquierdo.min_temp)
            nodo.max_temp = max(nodo.max_temp, nodo.izquierdo.max_temp)
        
        if nodo.derecho:
            nodo.min_temp = min(nodo.min_temp, nodo.derecho.min_temp)
            nodo.max_temp = max(nodo.max_temp, nodo.derecho.max_temp)
    
    # ============ ROTACIONES AVL ============
    
    def _rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        """Rotación simple a la derecha"""
        x = y.izquierdo
        T2 = x.derecho
        
        x.derecho = y
        y.izquierdo = T2
        
        self._actualizar_altura(y)
        self._actualizar_extremos(y)
        self._actualizar_altura(x)
        self._actualizar_extremos(x)
        
        return x
    
    def _rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        """Rotación simple a la izquierda"""
        y = x.derecho
        T2 = y.izquierdo
        
        y.izquierdo = x
        x.derecho = T2
        
        self._actualizar_altura(x)
        self._actualizar_extremos(x)
        self._actualizar_altura(y)
        self._actualizar_extremos(y)
        
        return y
    
    # ============ OPERACIONES PRINCIPALES ============
    
    def guardar_temperatura(self, temperatura: float, fecha: str):
        """
        Guarda la medida de temperatura asociada a la fecha.
        Si la fecha ya existe, actualiza la temperatura.
        
        Args:
            temperatura: Valor de temperatura en ºC
            fecha: Fecha en formato "dd/mm/aaaa"
        """
        fecha_dt = self._str_a_fecha(fecha)
        self.raiz = self._insertar(self.raiz, fecha_dt, temperatura)
    
    def _insertar(self, nodo: Optional[NodoAVL], fecha: datetime, temperatura: float) -> NodoAVL:
        """Inserción recursiva con balanceo AVL"""
        # Inserción BST estándar
        if not nodo:
            self.cantidad += 1
            return NodoAVL(fecha, temperatura)
        
        if fecha < nodo.fecha:
            nodo.izquierdo = self._insertar(nodo.izquierdo, fecha, temperatura)
        elif fecha > nodo.fecha:
            nodo.derecho = self._insertar(nodo.derecho, fecha, temperatura)
        else:
            # Fecha duplicada: actualizar temperatura
            nodo.temperatura = temperatura
            self._actualizar_extremos(nodo)
            return nodo
        
        # Actualizar altura y extremos
        self._actualizar_altura(nodo)
        self._actualizar_extremos(nodo)
        
        # Balancear
        balance = self._balance(nodo)
        
        # Caso Izquierda-Izquierda
        if balance > 1 and fecha < nodo.izquierdo.fecha:
            return self._rotar_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and fecha > nodo.derecho.fecha:
            return self._rotar_izquierda(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and fecha > nodo.izquierdo.fecha:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and fecha < nodo.derecho.fecha:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def devolver_temperatura(self, fecha: str) -> Optional[float]:
        """
        Devuelve la medida de temperatura en la fecha determinada.
        
        Args:
            fecha: Fecha en formato "dd/mm/aaaa"
            
        Returns:
            Temperatura en ºC o None si no existe
        """
        fecha_dt = self._str_a_fecha(fecha)
        nodo = self._buscar(self.raiz, fecha_dt)
        return nodo.temperatura if nodo else None
    
    def _buscar(self, nodo: Optional[NodoAVL], fecha: datetime) -> Optional[NodoAVL]:
        """Búsqueda binaria recursiva"""
        if not nodo or nodo.fecha == fecha:
            return nodo
        
        if fecha < nodo.fecha:
            return self._buscar(nodo.izquierdo, fecha)
        else:
            return self._buscar(nodo.derecho, fecha)
    
    def max_temp_rango(self, fecha1: str, fecha2: str) -> Optional[float]:
        """
        Devuelve la temperatura máxima entre fecha1 y fecha2 inclusive.
        
        Args:
            fecha1: Fecha inicial en formato "dd/mm/aaaa"
            fecha2: Fecha final en formato "dd/mm/aaaa"
            
        Returns:
            Temperatura máxima en el rango o None si no hay datos
        """
        fecha1_dt = self._str_a_fecha(fecha1)
        fecha2_dt = self._str_a_fecha(fecha2)
        return self._max_rango(self.raiz, fecha1_dt, fecha2_dt)
    
    def _max_rango(self, nodo: Optional[NodoAVL], fecha1: datetime, fecha2: datetime) -> Optional[float]:
        """Búsqueda recursiva de máximo en rango con poda"""
        if not nodo:
            return None
        
        # Si el nodo está fuera del rango por la izquierda
        if nodo.fecha < fecha1:
            return self._max_rango(nodo.derecho, fecha1, fecha2)
        
        # Si el nodo está fuera del rango por la derecha
        if nodo.fecha > fecha2:
            return self._max_rango(nodo.izquierdo, fecha1, fecha2)
        
        # El nodo está en el rango
        max_temp = nodo.temperatura
        
        # Buscar en subárbol izquierdo
        if nodo.izquierdo:
            max_izq = self._max_rango(nodo.izquierdo, fecha1, fecha2)
            if max_izq is not None:
                max_temp = max(max_temp, max_izq)
        
        # Buscar en subárbol derecho
        if nodo.derecho:
            max_der = self._max_rango(nodo.derecho, fecha1, fecha2)
            if max_der is not None:
                max_temp = max(max_temp, max_der)
        
        return max_temp
    
    def min_temp_rango(self, fecha1: str, fecha2: str) -> Optional[float]:
        """
        Devuelve la temperatura mínima entre fecha1 y fecha2 inclusive.
        
        Args:
            fecha1: Fecha inicial en formato "dd/mm/aaaa"
            fecha2: Fecha final en formato "dd/mm/aaaa"
            
        Returns:
            Temperatura mínima en el rango o None si no hay datos
        """
        fecha1_dt = self._str_a_fecha(fecha1)
        fecha2_dt = self._str_a_fecha(fecha2)
        return self._min_rango(self.raiz, fecha1_dt, fecha2_dt)
    
    def _min_rango(self, nodo: Optional[NodoAVL], fecha1: datetime, fecha2: datetime) -> Optional[float]:
        """Búsqueda recursiva de mínimo en rango con poda"""
        if not nodo:
            return None
        
        # Si el nodo está fuera del rango por la izquierda
        if nodo.fecha < fecha1:
            return self._min_rango(nodo.derecho, fecha1, fecha2)
        
        # Si el nodo está fuera del rango por la derecha
        if nodo.fecha > fecha2:
            return self._min_rango(nodo.izquierdo, fecha1, fecha2)
        
        # El nodo está en el rango
        min_temp = nodo.temperatura
        
        # Buscar en subárbol izquierdo
        if nodo.izquierdo:
            min_izq = self._min_rango(nodo.izquierdo, fecha1, fecha2)
            if min_izq is not None:
                min_temp = min(min_temp, min_izq)
        
        # Buscar en subárbol derecho
        if nodo.derecho:
            min_der = self._min_rango(nodo.derecho, fecha1, fecha2)
            if min_der is not None:
                min_temp = min(min_temp, min_der)
        
        return min_temp
    
    def temp_extremos_rango(self, fecha1: str, fecha2: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Devuelve la temperatura mínima y máxima entre fecha1 y fecha2 inclusive.
        
        Args:
            fecha1: Fecha inicial en formato "dd/mm/aaaa"
            fecha2: Fecha final en formato "dd/mm/aaaa"
            
        Returns:
            Tupla (temperatura_mínima, temperatura_máxima)
        """
        return (self.min_temp_rango(fecha1, fecha2), self.max_temp_rango(fecha1, fecha2))
    
    def borrar_temperatura(self, fecha: str):
        """
        Elimina del árbol la medición correspondiente a esa fecha.
        
        Args:
            fecha: Fecha en formato "dd/mm/aaaa"
        """
        fecha_dt = self._str_a_fecha(fecha)
        self.raiz = self._eliminar(self.raiz, fecha_dt)
    
    def _eliminar(self, nodo: Optional[NodoAVL], fecha: datetime) -> Optional[NodoAVL]:
        """Eliminación recursiva con balanceo AVL"""
        if not nodo:
            return None
        
        # Buscar el nodo a eliminar
        if fecha < nodo.fecha:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, fecha)
        elif fecha > nodo.fecha:
            nodo.derecho = self._eliminar(nodo.derecho, fecha)
        else:
            # Nodo encontrado
            self.cantidad -= 1
            
            # Caso 1: Nodo sin hijos o con un hijo
            if not nodo.izquierdo:
                return nodo.derecho
            elif not nodo.derecho:
                return nodo.izquierdo
            
            # Caso 2: Nodo con dos hijos
            # Encontrar el sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._min_nodo(nodo.derecho)
            nodo.fecha = sucesor.fecha
            nodo.temperatura = sucesor.temperatura
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.fecha)
        
        # Actualizar altura y extremos
        self._actualizar_altura(nodo)
        self._actualizar_extremos(nodo)
        
        # Balancear
        balance = self._balance(nodo)
        
        # Caso Izquierda-Izquierda
        if balance > 1 and self._balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)
        
        # Caso Izquierda-Derecha
        if balance > 1 and self._balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)
        
        # Caso Derecha-Derecha
        if balance < -1 and self._balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)
        
        # Caso Derecha-Izquierda
        if balance < -1 and self._balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _min_nodo(self, nodo: NodoAVL) -> NodoAVL:
        """Encuentra el nodo con la fecha mínima en el subárbol"""
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual
    
    def devolver_temperaturas(self, fecha1: str, fecha2: str) -> List[str]:
        """
        Devuelve un listado de las mediciones en el rango ordenado por fechas.
        
        Args:
            fecha1: Fecha inicial en formato "dd/mm/aaaa"
            fecha2: Fecha final en formato "dd/mm/aaaa"
            
        Returns:
            Lista de strings con formato "dd/mm/aaaa: temperatura ºC"
        """
        fecha1_dt = self._str_a_fecha(fecha1)
        fecha2_dt = self._str_a_fecha(fecha2)
        resultado = []
        self._inorden_rango(self.raiz, fecha1_dt, fecha2_dt, resultado)
        return resultado
    
    def _inorden_rango(self, nodo: Optional[NodoAVL], fecha1: datetime, fecha2: datetime, resultado: List[str]):
        """Recorrido inorden del rango con poda"""
        if not nodo:
            return
        
        # Recorrer izquierdo si puede haber nodos en el rango
        if nodo.fecha > fecha1:
            self._inorden_rango(nodo.izquierdo, fecha1, fecha2, resultado)
        
        # Procesar nodo actual si está en el rango
        if fecha1 <= nodo.fecha <= fecha2:
            fecha_str = self._fecha_a_str(nodo.fecha)
            resultado.append(f"{fecha_str}: {nodo.temperatura} ºC")
        
        # Recorrer derecho si puede haber nodos en el rango
        if nodo.fecha < fecha2:
            self._inorden_rango(nodo.derecho, fecha1, fecha2, resultado)
    
    def cantidad_muestras(self) -> int:
        """
        Devuelve la cantidad de muestras de la BD.
        
        Returns:
            Número de mediciones almacenadas
        """
        return self.cantidad
    
    # ============ CARGA DESDE ARCHIVO ============
    
    def cargar_desde_archivo(self) -> Tuple[int, int]:
        """
        Lee el archivo 'muestras.txt' y carga las temperaturas a la base de datos.
        
        Formato esperado: YYYY-MM-DD;temperatura (una medición por línea)
        Detecta automáticamente el encoding (UTF-8, UTF-16, etc.)
        
        Returns:
            Tupla (líneas_procesadas, registros_cargados)
        """
        # Detectar encoding automáticamente
        texto = None
        for enc in ('utf-8', 'utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1'):
            try:
                with open('muestras.txt', 'r', encoding=enc) as archivo:
                    texto = archivo.read()
                    break
            except FileNotFoundError:
                raise
            except Exception:
                continue
        
        if texto is None:
            raise RuntimeError("No se pudo leer el archivo 'muestras.txt' con los encodings probados")
        
        lineas_procesadas = 0
        registros_cargados = 0
        
        for linea in texto.splitlines():
            original = linea
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            
            lineas_procesadas += 1
            
            try:
                # Detectar separador
                if ';' in linea:
                    partes = linea.split(';')
                elif ',' in linea:
                    partes = linea.split(',')
                else:
                    continue
                
                if len(partes) < 2:
                    continue
                
                fecha_str = partes[0].strip()
                temp_str = partes[1].strip()
                # limpiar sufijos de temperatura: "ºC", " C", etc.
                temp_str = temp_str.replace('ºC', '').replace('°C', '').replace(' C', '').replace('c', '').strip()
                temperatura = float(temp_str)
                
                # Detectar formato de fecha
                if '-' in fecha_str and len(fecha_str) == 10:
                    # Formato YYYY-MM-DD
                    dt = datetime.strptime(fecha_str, '%Y-%m-%d')
                    fecha_ddmmyyyy = dt.strftime('%d/%m/%Y')
                elif '/' in fecha_str:
                    # Formato dd/mm/aaaa
                    # Validar que sea correcto
                    dt = datetime.strptime(fecha_str, '%d/%m/%Y')
                    fecha_ddmmyyyy = dt.strftime('%d/%m/%Y')
                else:
                    continue
                
                self.guardar_temperatura(temperatura, fecha_ddmmyyyy)
                registros_cargados += 1
                
            except Exception:
                # Ignorar líneas con errores
                # print(f"Línea ignorada: {original}")  # opcional para debug
                continue
        
        return (lineas_procesadas, registros_cargados)