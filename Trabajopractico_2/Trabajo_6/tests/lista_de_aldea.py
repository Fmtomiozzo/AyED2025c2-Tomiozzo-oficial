import os
from modules.lector import leer_aristas_csv_comas, ALDEAS_FILE
from modules.grafos import grafo_no_dirigido, alcanzables, mst_prim, enraizar_mst

ORIGEN = "Peligros"


def main():
    # 1) Verificar archivo
    if not os.path.isfile(ALDEAS_FILE):
        raise SystemExit(f"No se encontró el archivo de aldeas en: {ALDEAS_FILE}")

    # 2) Leer aristas
    edges = leer_aristas_csv_comas(ALDEAS_FILE)
    if not edges:
        raise SystemExit("No se pudieron leer aristas del archivo.")

    # 3) Construir grafo no dirigido
    adj, nodos = grafo_no_dirigido(edges)

    if ORIGEN not in nodos:
        raise SystemExit(f"No existe la aldea origen '{ORIGEN}' en el archivo.")

    # 4) (opcional) comprobar alcanzables
    R = alcanzables(adj, ORIGEN)
    if not R:
        raise SystemExit("No hay aldeas alcanzables desde el origen.")

    # 5) Calcular MST con Prim
    mst, total = mst_prim(adj, ORIGEN)

    # Validación simple: si el MST no conectó todos los alcanzables
    esperadas = max(0, len(R) - 1)
    if len(mst) != esperadas:
        print(f"AVISO: el MST encontrado tiene {len(mst)} aristas, se esperaban {esperadas} para {len(R)} nodos alcanzables.")
        # No cortamos el programa, solo avisamos.

    # 6) Enraizar MST
    parent, children, N = enraizar_mst(mst, ORIGEN)
    if ORIGEN not in parent:
        parent[ORIGEN] = (None, 0)
        children.setdefault(ORIGEN, [])
        N.add(ORIGEN)

    # 7) Salidas
    print("1) Aldeas alcanzables (alfabético):")
    for n in sorted(N):
        print(f" - {n}")

    print(f"\n2) Plan de distribución (enraizado en '{ORIGEN}'):")
    for n in sorted(N):
        p, w = parent.get(n, (None, 0))
        recibe = "(origen)" if p is None else f"{p} (dist={w})"
        env = ", ".join(f"{h} (dist={dw})" for h, dw in children.get(n, [])) or "(sin reenvíos)"
        print(f" - {n}: recibe de {recibe}; envía a: {env}")

    print(f"\n3) Suma total de distancias (peso MST - Prim): {total}")


if __name__ == "__main__":
    main()