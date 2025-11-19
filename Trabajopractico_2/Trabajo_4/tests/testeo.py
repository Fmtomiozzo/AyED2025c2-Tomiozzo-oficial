# tests/testeo.py

import time
import datetime
import random

from modules.paciente import Paciente
from modules.cola_prioridad import ColaPrioridad

# --- Configuración de la simulación ---
N_CICLOS_SIMULACION = 20
PROBABILIDAD_ATENCION = 0.5

# --- Inicialización ---
sala_de_espera = ColaPrioridad()

print("--- INICIANDO SIMULACIÓN DE SALA DE EMERGENCIAS ---")

# --- Bucle principal de la simulación ---
for i in range(N_CICLOS_SIMULACION):
    # 1) Mostrar el momento actual de la simulación
    ahora = datetime.datetime.now()
    fecha_y_hora = ahora.strftime('%d/%m/%Y %H:%M:%S')
    print('\n' + '___' * 15)
    print(f"\n[{fecha_y_hora}] --- CICLO {i+1}/{N_CICLOS_SIMULACION} ---")

    # 2) Llega un nuevo paciente
    nuevo_paciente = Paciente()
    sala_de_espera.insertar(nuevo_paciente.get_riesgo(), nuevo_paciente)
    print(f"  -> Llega nuevo paciente: {nuevo_paciente}")

    # 3) Mostrar quién sería el próximo a atender (sin sacarlo de la cola)
    if not sala_de_espera.esta_vacia():
        proximo_a_atender = sala_de_espera.ver_proximo()
        print(f"  -> Próximo a atender (sin extraer): {proximo_a_atender}")
    else:
        print("  -> No hay pacientes en espera para ver el próximo.")

    # 4) Decidir si se atiende a un paciente en este ciclo
    if random.random() < PROBABILIDAD_ATENCION and not sala_de_espera.esta_vacia():
        paciente_atendido = sala_de_espera.extraer()
        print('\n' + '__' * 40)
        print(f" SE ATIENDE EL PACIENTE CON MÁXIMA PRIORIDAD: {paciente_atendido}")
        print('__' * 40)
    else:
        print("\n  El Doctor está ocupado o no hay pacientes (no se atiende en este ciclo).")

    # 5) Mostrar el estado actual de la sala de espera
    print(f"\n  Pacientes en sala de espera: {sala_de_espera.tamano()}")
    if not sala_de_espera.esta_vacia():
        print("  Cola (de más urgente a menos urgente):")
        for p_en_espera in sala_de_espera.ver_todos():
            print(f"    - {p_en_espera}")
    else:
        print("    (No hay pacientes en espera)")

    print('___' * 15)

    # 6) Pausa para simular el paso del tiempo
    time.sleep(1)

print("\n--- FIN DE LA SIMULACIÓN ---")
print(f"Pacientes restantes en sala de espera: {sala_de_espera.tamano()}")
if not sala_de_espera.esta_vacia():
    print("Detalle de pacientes restantes:")
    for p_final in sala_de_espera.ver_todos():
        print(f"  - {p_final}")