from modules.temperaturas_db import Temperaturas_DB   # Importa la clase de la BD AVL

def main():
    db = Temperaturas_DB()                    # Crea instancia de la BD

    # Carga desde archivo
    try:
        lineas_procesadas, registros_cargados = db.cargar_desde_archivo()  # Carga datos y devuelve métricas
        print(f"lineas_procesadas: {lineas_procesadas}, registros_cargados: {registros_cargados}")  # Muestra métricas
    except FileNotFoundError:
        print("Error: no se encontró 'muestras.txt'")      # Manejo si falta el archivo
        return
    except Exception as e:
        print(f"Error al cargar: {e}")                      # Manejo de otros errores
        return

    # cantidad_muestras() (fechas únicas en el árbol)
    print(f"cantidad_muestras: {db.cantidad_muestras()}")  # Imprime cuántas muestras hay

    # Prueba básica de guardar_temperatura y devolver_temperatura
    fecha_nueva = "15/03/2025"                             # Fecha de prueba (dd/mm/aaaa)
    db.guardar_temperatura(25.0, fecha_nueva)              # Inserta/actualiza temperatura para esa fecha
    print(f"devolver_temperatura ('{fecha_nueva}'): {db.devolver_temperatura(fecha_nueva)}")  # Consulta por fecha

    # Consultas de rango: ejemplo Febrero 2025
    f1, f2 = "01/02/2025", "28/02/2025"                    # Define rango de fechas (inclusive)
    print(f"min_temp_rango ('{f1}','{f2}'): {db.min_temp_rango(f1, f2)}")  # Mínima en el rango
    print(f"max_temp_rango ('{f1}','{f2}'): {db.max_temp_rango(f1, f2)}")  # Máxima en el rango
    print(f"temp_extremos_rango ('{f1}','{f2}'): {db.temp_extremos_rango(f1, f2)}")  # (min, max) en el rango

    # devolver_temperaturas (formato “dd/mm/aaaa: temperatura ºC”)
    temps_list = db.devolver_temperaturas(f1, f2)          # Lista formateada de mediciones en el rango
    print(f"devolver_temperaturas ('{f1}','{f2}') (n={len(temps_list)}):")  # Muestra cantidad de items
    for s in temps_list:
        print(s)                                           # Imprime cada medición formateada

    # borrar_temperatura y verificación
    fecha_borrar = fecha_nueva                             # Selecciona la fecha insertada para borrar
    borrado = db.borrar_temperatura(fecha_borrar)          # Borra la medición de esa fecha
    print(f"borrar_temperatura ('{fecha_borrar}'): {borrado}")              # Indica si se borró
    print(f"devolver_temperatura ('{fecha_borrar}'): {db.devolver_temperatura(fecha_borrar)}")  # Verifica borrado

    # cantidad_muestras final (fechas únicas luego de borrar/insertar)
    print(f"cantidad_muestras: {db.cantidad_muestras()}")  # Reimprime total de muestras

if __name__ == "__main__":
    main()                                                 # Punto de entrada del script