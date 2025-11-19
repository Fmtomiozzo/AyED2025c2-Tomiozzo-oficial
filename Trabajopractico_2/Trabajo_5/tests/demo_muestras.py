from modules.temperaturas_db import Temperaturas_DB

def main():
    db = Temperaturas_DB()

    # Carga desde archivo
    try:
        lineas_procesadas, registros_cargados = db.cargar_desde_archivo()
        print(f"lineas_procesadas: {lineas_procesadas}, registros_cargados: {registros_cargados}")
    except FileNotFoundError:
        print("Error: no se encontró 'muestras.txt'")
        return
    except Exception as e:
        print(f"Error al cargar: {e}")
        return

    # cantidad_muestras()
    print(f"cantidad_muestras: {db.cantidad_muestras()}")

    # Prueba básica de guardar_temperatura y devolver_temperatura
    fecha_nueva = "15/03/2025"
    db.guardar_temperatura(25.0, fecha_nueva)
    print(f"devolver_temperatura ('{fecha_nueva}'): {db.devolver_temperatura(fecha_nueva)}")

    # Consultas de rango: ejemplo Febrero 2025
    f1, f2 = "01/02/2025", "28/02/2025"
    print(f"min_temp_rango ('{f1}','{f2}'): {db.min_temp_rango(f1, f2)}")
    print(f"max_temp_rango ('{f1}','{f2}'): {db.max_temp_rango(f1, f2)}")
    print(f"temp_extremos_rango ('{f1}','{f2}'): {db.temp_extremos_rango(f1, f2)}")

    # devolver_temperaturas
    temps_list = db.devolver_temperaturas(f1, f2)
    print(f"devolver_temperaturas ('{f1}','{f2}') (n={len(temps_list)}):")
    for s in temps_list:
        print(s)

    # borrar_temperatura y verificación
    fecha_borrar = fecha_nueva
    borrado = db.borrar_temperatura(fecha_borrar)
    print(f"borrar_temperatura ('{fecha_borrar}'): {borrado}")
    print(f"devolver_temperatura ('{fecha_borrar}'): {db.devolver_temperatura(fecha_borrar)}")

    # cantidad_muestras final
    print(f"cantidad_muestras: {db.cantidad_muestras()}")

if __name__ == "__main__":
    main()