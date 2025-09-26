#Ordenamiento burbuja: es uno de los mas faciles, pero poco eficiente ya que hace hace muchas operaciones para lograr ordenar los elementos.
    #tiene un espacio de memoria auxiliar (burbuja) donde se guarda el valor mayor.
    #en cada recorrido hay una comparacion menos.

#Ordenamiento quicksort: es muy eficiente, divide la lista en sublistas y se ordenan individualmente.
    #se usa la recursividad, hasta tener listas de solo dos elementos a comparar.
    #necesita indices.
    #usa menos operaciones pero mas memoria.

import time
import random
import matplotlib.pyplot as plt
from modules.burbuja import Burbuja
from modules.quicksort import Quicksort
from modules.radix_sort import Radix_sort
import random
from modules.quicksort import Quicksort

for i in range (500):
    lista = [random.randint(10000, 99999) for _ in range(500)]
    
ordenamiento= Burbuja(lista)
ordenamiento1 = Quicksort(lista)
ordenamiento2 = Radix_sort(lista)

def medir_tiempos():
    tamaños = list(range(1, 1001, 100))  # Tamaños de lista de 1 a 1000, incrementos de 100
    tiempos_burbuja = []
    tiempos_quicksort = []
    tiempos_radix = []
    tiempos_sorted = []

    for tamaño in tamaños:
        lista = [random.randint(0, 1000) for _ in range(tamaño)]

        # Medir Burbuja
        burbuja = Burbuja(lista.copy())
        inicio = time.perf_counter()
        burbuja.ordenar_lista()
        tiempos_burbuja.append(time.perf_counter() - inicio)

        # Medir Quicksort
        quicksort = Quicksort(lista.copy())
        inicio = time.perf_counter()
        quicksort.ordenar()
        tiempos_quicksort.append(time.perf_counter() - inicio)

        # Medir Radix Sort
        radix = Radix_sort(lista.copy())
        inicio = time.perf_counter()
        radix.ordenar()
        tiempos_radix.append(time.perf_counter() - inicio)
        #print(f"Tiempos Radix: {tiempos_radix}")
        # Medir sorted
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
    plt.title('Comparación de Tiempos de Ejecución de Algoritmos de Ordenamiento')
    plt.legend()
    plt.grid()
    plt.show()

medir_tiempos()