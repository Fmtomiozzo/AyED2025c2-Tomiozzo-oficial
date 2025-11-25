# Comparación de algoritmos de ordenamiento:
# - Burbuja
# - Quicksort
# - Radix Sort
# - sorted() de Python

import time
import random
import matplotlib.pyplot as plt

from modules.burbuja import Burbuja
from modules.quicksort import Quicksort
from modules.radix_sort import Radix_sort


def medir_tiempos():
    tamaños = list(range(100, 1001, 100))  # Tamaños de lista de 100 a 1000
    tiempos_burbuja = []
    tiempos_quicksort = []
    tiempos_radix = []
    tiempos_sorted = []

    for tamaño in tamaños:
        lista = [random.randint(0, 1000) for _ in range(tamaño)]

        # Burbuja
        burbuja = Burbuja(lista.copy())
        inicio = time.perf_counter()
        burbuja.ordenar_lista()
        tiempos_burbuja.append(time.perf_counter() - inicio)

        # Quicksort
        quicksort = Quicksort(lista.copy())
        inicio = time.perf_counter()
        quicksort.ordenar()
        tiempos_quicksort.append(time.perf_counter() - inicio)

        # Radix Sort
        radix = Radix_sort(lista.copy())
        inicio = time.perf_counter()
        radix.ordenar()
        tiempos_radix.append(time.perf_counter() - inicio)

        # sorted de Python
        inicio = time.perf_counter()
        sorted(lista.copy())
        tiempos_sorted.append(time.perf_counter() - inicio)

    # Graficar resultados
    plt.figure(figsize=(10, 6))
    plt.plot(tamaños, tiempos_burbuja, label='Burbuja', marker='o')
    plt.plot(tamaños, tiempos_quicksort, label='Quicksort', marker='o')
    plt.plot(tamaños, tiempos_radix, label='Radix Sort', marker='o')
    plt.plot(tamaños, tiempos_sorted, label='sorted() de Python', marker='o')
    plt.xlabel('Tamaño de la lista')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Comparación de Tiempos de Algoritmos de Ordenamiento')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    medir_tiempos()