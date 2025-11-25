import time
import matplotlib.pyplot as plt
import numpy as np

from Listadobleenlazada import ListaDobleEnlazada
# o bien: from modules.Listadobleenlazada import ListaDobleEnlazada
# según tu estructura

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

if __name__ == "__main__":
    # Realizar las mediciones
    tamanios, tiempos_len, tiempos_copiar, tiempos_invertir = realizar_mediciones()

    # ==== Gráfica 1: len() en MICROSEGUNDOS ====
    plt.figure(figsize=(8, 5))
    plt.plot(tamanios, [t * 1e6 for t in tiempos_len], 'bo-', linewidth=2, markersize=6)
    plt.title('Método len() - O(1)', fontsize=12, fontweight='bold')
    plt.xlabel('Número de elementos (N)')
    plt.ylabel('Tiempo (microsegundos)')
    plt.grid(True, alpha=0.3)
    plt.show()

    # ==== Gráficas individuales en SEGUNDOS ====
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

    # ==== Valores en tabla ====
    print("\n=== ANÁLISIS DE RESULTADOS ===")
    print(f"Tamaños probados: {tamanios}")
    print(f"\nTiempos len() (microsegundos): {[f'{t * 1e6:.2f}' for t in tiempos_len]}")
    print(f"Tiempos len() (segundos): {[f'{t:.8f}' for t in tiempos_len]}")
    print(f"Tiempos copiar() (segundos): {[f'{t:.6f}' for t in tiempos_copiar]}")
    print(f"Tiempos invertir() (segundos): {[f'{t:.6f}' for t in tiempos_invertir]}")