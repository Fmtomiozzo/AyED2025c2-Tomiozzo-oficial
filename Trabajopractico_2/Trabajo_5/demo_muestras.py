"""
Demo de Temperaturas_DB con archivo muestras.txt
Programa de prueba que carga datos desde archivo y realiza consultas de ejemplo.
"""

from temperaturas_db import Temperaturas_DB
from datetime import datetime
from typing import List, Tuple


def recolectar_todas(db: Temperaturas_DB) -> List[Tuple[datetime, float]]:
    """Recolecta todas las mediciones del árbol en orden"""
    pares = []
    
    def _recolectar(nodo):
        if not nodo:
            return
        _recolectar(nodo.izquierdo)
        pares.append((nodo.fecha, nodo.temperatura))
        _recolectar(nodo.derecho)
    
    _recolectar(db.raiz)
    return pares


def main():
    print("=" * 70)
    print("SISTEMA DE BASE DE DATOS DE TEMPERATURAS - Kevin Kelvin")
    print("Implementación con Árbol AVL")
    print("=" * 70)
    
    # Crear base de datos
    db = Temperaturas_DB()
    
    # Cargar archivo muestras.txt
    print("\n1. CARGA DE DATOS DESDE ARCHIVO")
    print("-" * 70)
    
    try:
        lineas_proc, registros_ok = db.cargar_desde_archivo()
        print("✓ Archivo 'muestras.txt' cargado exitosamente")
        print(f"  - Líneas procesadas: {lineas_proc}")
        print(f"  - Registros cargados: {registros_ok}")
        print(f"  - Cantidad de muestras en BD: {db.cantidad_muestras()}")
    except FileNotFoundError:
        print("✗ Error: No se encontró el archivo 'muestras.txt'")
        print("  Asegúrate de que el archivo esté en la misma carpeta que este script.")
        return
    except Exception as e:
        print(f"✗ Error al cargar archivo: {e}")
        return
    
    if db.cantidad_muestras() == 0:
        print("\n✗ No hay datos para procesar.")
        return
    
    # Recolectar todas las mediciones
    pares = recolectar_todas(db)
    
    # Resumen del dataset
    print("\n2. RESUMEN DEL DATASET")
    print("-" * 70)
    fecha_min = min(pares, key=lambda x: x[0])[0]
    fecha_max = max(pares, key=lambda x: x[0])[0]
    temp_min_par = min(pares, key=lambda x: x[1])
    temp_max_par = max(pares, key=lambda x: x[1])
    
    print(f"Rango de fechas: {fecha_min.strftime('%d/%m/%Y')} a {fecha_max.strftime('%d/%m/%Y')}")
    print(f"Temperatura mínima: {temp_min_par[1]} ºC en {temp_min_par[0].strftime('%d/%m/%Y')}")
    print(f"Temperatura máxima: {temp_max_par[1]} ºC en {temp_max_par[0].strftime('%d/%m/%Y')}")
    
    # Consultar temperatura específica
    print("\n3. CONSULTAR TEMPERATURA ESPECÍFICA")
    print("-" * 70)
    fecha_consulta = pares[len(pares)//2][0].strftime('%d/%m/%Y')  # Fecha del medio
    temp = db.devolver_temperatura(fecha_consulta)
    print(f"Temperatura en {fecha_consulta}: {temp} ºC")
    
    # Consulta por rango: Febrero 2025
    print("\n4. CONSULTA POR RANGO - FEBRERO 2025")
    print("-" * 70)
    fecha1, fecha2 = "01/02/2025", "28/02/2025"
    print(f"Rango consultado: {fecha1} a {fecha2}")
    
    min_temp = db.min_temp_rango(fecha1, fecha2)
    max_temp = db.max_temp_rango(fecha1, fecha2)
    temperaturas = db.devolver_temperaturas(fecha1, fecha2)
    
    print(f"  - Temperatura mínima: {min_temp} ºC")
    print(f"  - Temperatura máxima: {max_temp} ºC")
    print(f"  - Cantidad de mediciones: {len(temperaturas)}")
    
    # Mostrar primeras 5 del rango
    print("\n  Primeras 5 mediciones del rango:")
    for i, temp_str in enumerate(temperaturas[:5], 1):
        print(f"    {i}. {temp_str}")
    
    if len(temperaturas) > 5:
        print(f"    ... ({len(temperaturas) - 5} mediciones más)")
    
    # Consulta de extremos en rango
    print("\n5. EXTREMOS EN RANGO - MARZO 2025")
    print("-" * 70)
    fecha1, fecha2 = "01/03/2025", "31/03/2025"
    print(f"Rango consultado: {fecha1} a {fecha2}")
    
    min_t, max_t = db.temp_extremos_rango(fecha1, fecha2)
    print(f"  - Temperatura mínima: {min_t} ºC")
    print(f"  - Temperatura máxima: {max_t} ºC")
    
    # Listado de mediciones (primeras y últimas)
    print("\n6. LISTADO DE MEDICIONES")
    print("-" * 70)
    print("Primeras 10 mediciones (ordenadas por fecha):")
    for i, (fecha, temp) in enumerate(pares[:10], 1):
        print(f"  {i:2d}. {fecha.strftime('%d/%m/%Y')}: {temp} ºC")
    
    print("\nÚltimas 10 mediciones:")
    for i, (fecha, temp) in enumerate(pares[-10:], 1):
        print(f"  {i:2d}. {fecha.strftime('%d/%m/%Y')}: {temp} ºC")
    
    # Prueba de borrado
    print("\n7. PRUEBA DE BORRADO")
    print("-" * 70)
    fecha_borrar = pares[0][0].strftime('%d/%m/%Y')
    print(f"Cantidad de muestras antes de borrar: {db.cantidad_muestras()}")
    print(f"Borrando medición del {fecha_borrar}...")
    db.borrar_temperatura(fecha_borrar)
    print(f"Cantidad de muestras después de borrar: {db.cantidad_muestras()}")
    temp_borrada = db.devolver_temperatura(fecha_borrar)
    print(f"Verificación (debe ser None): {temp_borrada}")
    
    # Análisis de complejidad
    print("\n8. ANÁLISIS DE COMPLEJIDAD BIG-O")
    print("-" * 70)
    print("| Método                    | Complejidad  | Explicación")
    print("|" + "-" * 27 + "|" + "-" * 14 + "|" + "-" * 50)
    print("| guardar_temperatura       | O(log n)     | Inserción en AVL balanceado")
    print("| devolver_temperatura      | O(log n)     | Búsqueda binaria en árbol")
    print("| max_temp_rango            | O(k + log n) | k = nodos en rango, con poda")
    print("| min_temp_rango            | O(k + log n) | k = nodos en rango, con poda")
    print("| temp_extremos_rango       | O(k + log n) | Calcula min y max en un recorrido")
    print("| borrar_temperatura        | O(log n)     | Eliminación en AVL + rebalanceo")
    print("| devolver_temperaturas     | O(k + log n) | k = nodos en rango, inorden con poda")
    print("| cantidad_muestras         | O(1)         | Retorna contador mantenido")
    print("| cargar_desde_archivo      | O(m log n)   | m = líneas, cada inserción O(log n)")
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()