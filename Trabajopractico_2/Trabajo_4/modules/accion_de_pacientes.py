# -*- coding: utf-8 -*-
"""
Sala de emergencias con Cola de Prioridad (Heap)
- Objetivo: almacenar pacientes conforme ingresan y garantizar que al atender,
  siempre salga el de mayor prioridad clínica (más delicado).
- Criterio de prioridad: (nivel_de_riesgo, orden_de_llegada)
  * nivel_de_riesgo: número entero donde menor valor = más urgente (p.ej., 1 crítico, 5 leve).
  * orden_de_llegada: contador incremental para desempatar (FIFO) en caso de mismo riesgo.
- Estructura: min-heap (heapq) de Python, que siempre mantiene en la cima
  el menor elemento según la tupla de prioridad.
- Complejidad:
  * Inserción (heappush): O(log n)
  * Extracción del más prioritario (heappop): O(log n)
  * Consulta del próximo sin extraer (peek): O(1) accediendo a cola_de_espera[0]
- Nota: Este script es la "aplicación" (sala de emergencias). La estructura heap
  es genérica porque almacena tuplas (prioridad, desempate, objeto), y el objeto
  podría ser cualquier tipo, no solo pacientes.
"""

import time
import datetime
import heapq       # librería estándar de Python para min-heap (cola de prioridad)
import paciente as pac  # módulo provisto con la clase Paciente (no lo modificamos)
import random

# n controla cuántos ciclos de simulación se ejecutan (llegadas/atenciones)
n = 20

# Estructura principal: el heap (cola de prioridad).
# Guardamos tuplas de la forma (riesgo, orden_llegada, objeto_paciente)
cola_de_espera = []
heapq.heapify(cola_de_espera)  # convierte la lista en un heap válido

# Contador para desempatar por orden de llegada (FIFO cuando el riesgo es igual)
contador_llegada = 0

# Bucle principal de la simulación
for i in range(n):
    # 1) Timestamp (solo para visualizar en qué momento pasa cada evento)
    ahora = datetime.datetime.now()
    fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S')
    print('___' * 15)
    print('\n', fecha_y_hora, '\n')

    # 2) Llega un nuevo paciente desde paciente.py
    #    - Se instancia
    #    - Se incrementa el contador de llegada para garantizar estabilidad FIFO
    p = pac.Paciente()
    contador_llegada += 1

    # 3) Inserción al heap (cola de prioridad)
    #    - heappush mantiene la propiedad de heap en O(log n)
    #    - prioridad = (p.get_riesgo(), contador_llegada)
    #         * p.get_riesgo(): menor valor => más urgente
    #         * contador_llegada: desempate (el que llegó antes va primero si el riesgo es igual)
    #    - almacenamos el objeto paciente completo como tercer elemento (genérico)
    heapq.heappush(cola_de_espera, (p.get_riesgo(), contador_llegada, p))
    print("Llega nuevo paciente:", p)

    # 4) Consulta opcional del "próximo a atender" sin extraer (peek)
    #    - Acceder al tope del heap es O(1) leyendo el índice 0
    if cola_de_espera:
        proximo = cola_de_espera[0][2]  # [0] es la cima; [2] es el objeto Paciente
        print("Próximo a atender (sin extraer):", proximo)

    # 5) Decisión de atención (50% de probabilidad en cada ciclo)
    #    - Si corresponde atender y la cola no está vacía,
    #      extraemos con heappop (O(log n)) al más prioritario
    if random.random() < 0.5 and cola_de_espera:
        _, _, paciente_atendido = heapq.heappop(cola_de_espera)
        print('__' * 40)
        print("Se atiende el paciente (máxima prioridad):", paciente_atendido)
        print('__' * 40)
    else:
        print("El Doctor está ocupado (no se atiende en este ciclo).")

    print()

    # 6) Visualización del estado de la sala de espera
    #    - len(cola_de_espera): cuántos pacientes están aguardando
    #    - sorted(cola_de_espera): solo para mostrar en orden de prioridad;
    #      NO altera el heap (es una copia ordenada). Costo O(n log n) pero solo para display.
    print("Pacientes en sala de espera:", len(cola_de_espera))
    if cola_de_espera:
        print("Cola (de más urgente a menos urgente):")
        for _, _, paciente_en_espera in sorted(cola_de_espera):
            print("\t", paciente_en_espera)
    else:
        print("\t(No hay pacientes en espera)")

    print('___' * 15)

    # 7) Pausa para simular el paso del tiempo y hacer legible la salida
    time.sleep(1)

"""
Resumen para defensa oral:
- ¿Qué estructura usan? Un min-heap (heapq) como cola de prioridad.
- ¿Cómo definen la prioridad? Tupla (riesgo, llegada): menor riesgo = más urgente; ante empate, FIFO.
- ¿Por qué es genérica? El heap guarda tuplas (clave, desempate, item) y 'item' puede ser cualquier objeto.
- ¿Complejidad?
  * Inserción: O(log n)
  * Extracción del más prioritario: O(log n)
  * Consulta del próximo: O(1)
- ¿Qué garantiza? Siempre se atiende primero al paciente más delicado; ante empate, al que llegó antes.
"""