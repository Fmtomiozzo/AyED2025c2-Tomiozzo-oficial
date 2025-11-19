import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALDEAS_FILE = os.path.join(SCRIPT_DIR, "aldeas.txt")


def norm(s: str) -> str:
    """Normaliza espacios múltiples a uno y quita espacios extremos."""
    return " ".join(s.strip().split())


def leer_aristas_csv_comas(path: str = ALDEAS_FILE):
    """
    Lee aristas desde un archivo CSV separado por comas.
    Cada línea: origen, destino, peso.
    Devuelve una lista de tuplas (u, v, w).
    """
    edges = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            partes = [norm(p) for p in s.split(",")]
            if len(partes) < 3:
                continue
            a, b, w = partes[0], partes[1], partes[2]
            if not a or not b or not w:
                continue
            if a.lower() == "nan" or b.lower() == "nan" or w.lower() == "nan":
                continue
            try:
                w = int(w)
            except ValueError:
                continue
            if w <= 0:
                continue
            edges.append((a, b, w))
    return edges