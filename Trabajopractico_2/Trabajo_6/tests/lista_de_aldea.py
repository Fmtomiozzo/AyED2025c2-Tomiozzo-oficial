import os                                         # Manejo de rutas y archivos del sistema operativo
from collections import defaultdict, deque        # defaultdict para listas por defecto; deque para colas eficientes

# Directorio donde está este script (tests)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # Obtiene la carpeta del archivo actual

# Ruta absoluta a aldeas.txt dentro de la carpeta hermana "modules"
ALDEAS_FILE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "modules", "aldeas.txt"))  # Construye ../modules/aldeas.txt

ORIGEN = "Peligros"                               # Nombre de la aldea origen

def norm(s: str) -> str:
    return " ".join(s.strip().split())            # Normaliza espacios múltiples a uno y quita espacios extremos

def leer_aristas_csv_comas(path):
    edges = []                                    # Lista donde guardaremos aristas (u, v, w)
    with open(path, "r", encoding="utf-8") as f:  # Abre el archivo de texto en modo lectura
        for line in f:                             # Recorre cada línea del archivo
            s = line.strip()                      # Quita salto de línea y espacios afuera
            if not s:
                continue                          # Salta líneas vacías
            partes = [norm(p) for p in s.split(",")]  # Separa por comas y normaliza espacios
            if len(partes) < 3:
                continue                          # Necesita al menos 3 columnas: u, v, w
            a, b, w = partes[0], partes[1], partes[2]  # Asigna los campos
            if not a or not b or not w:
                continue                          # Salta si falta algún dato
            if a.lower() == "nan" or b.lower() == "nan" or w.lower() == "nan":
                continue                          # Ignora filas con 'nan'
            try:
                w = int(w)                        # Convierte el peso a entero
            except:
                continue                          # Si no se puede convertir, ignora la línea
            if w <= 0:
                continue                          # Ignora pesos no positivos
            edges.append((a, b, w))               # Agrega la arista válida a la lista
    return edges                                   # Devuelve todas las aristas leídas

def grafo_no_dirigido(edges):
    best = {}                                     # Mapa (par ordenado de nodos) -> menor peso visto
    nodos = set()                                 # Conjunto de nombres de aldeas
    for u, v, w in edges:                         # Recorre cada arista de entrada
        nodos.add(u); nodos.add(v)                # Registra los nodos en el conjunto
        k = tuple(sorted((u, v)))                 # Clave única del par sin dirección (u<=v)
        if k not in best or w < best[k]:
            best[k] = w                           # Guarda el menor peso para ese par
    adj = defaultdict(list)                       # Lista de adyacencia: nodo -> [(vecino, peso), ...]
    for (u, v), w in best.items():                # Recorre cada par único con su mejor peso
        adj[u].append((v, w))                     # Agrega arista u->v
        adj[v].append((u, w))                     # Agrega arista v->u (no dirigido)
    return adj, nodos                              # Devuelve la adyacencia y el set de nodos

class DSU:                                        # Disjoint Set Union (Union-Find) para Kruskal
    def __init__(self, S):
        self.p = {x: x for x in S}                # Padre de cada nodo: al inicio, él mismo
        self.r = {x: 0 for x in S}                # Rango (altura aproximada) inicia en 0
    def f(self, x):
        if self.p[x] != x:
            self.p[x] = self.f(self.p[x])         # Compresión de camino: apunta directo al representante
        return self.p[x]                           # Devuelve el representante del conjunto
    def u(self, a, b):
        a, b = self.f(a), self.f(b)               # Obtiene representantes de a y b
        if a == b: return False                   # Si ya están en el mismo conjunto, no une
        if self.r[a] < self.r[b]: a, b = b, a     # Unión por rango: el mayor rango queda como padre
        self.p[b] = a                             # Hace a padre de b
        if self.r[a] == self.r[b]: self.r[a] += 1 # Si rangos iguales, incrementa rango del nuevo padre
        return True                               # Indica que se unieron

def alcanzables(adj, s):
    vis = {s}                                     # Conjunto de visitados; arranca con el origen
    q = deque([s])                                # Cola para BFS inicializada con el origen
    while q:
        u = q.popleft()                           # Toma el primero de la cola
        for v, _ in adj[u]:                       # Recorre vecinos de u
            if v not in vis:
                vis.add(v); q.append(v)           # Marca como visitado y lo encola
    return vis                                    # Devuelve todos los nodos alcanzables desde s

def mst_kruskal(adj, R):
    E, seen = [], set()                           # E: aristas dentro de R; seen: pares ya agregados
    for u in R:
        for v, w in adj[u]:
            if v in R:                            # Considera aristas solo entre nodos alcanzables
                k = tuple(sorted((u, v)))         # Par no dirigido
                if k not in seen:
                    seen.add(k); E.append((u, v, w))  # Agrega arista única
    E.sort(key=lambda x: x[2])                    # Ordena aristas por peso ascendente
    dsu = DSU(R)                                  # Prepara estructura Union-Find
    mst, tot = [], 0                              # mst: aristas del árbol; tot: suma de pesos
    for u, v, w in E:
        if dsu.u(u, v):                           # Si unir u y v no forma ciclo
            mst.append((u, v, w)); tot += w       # Agrega arista al MST y suma su peso
    return mst, tot                                # Devuelve el MST y su peso total

def enraizar_mst(mst, raiz):
    g = defaultdict(list)                         # Adyacencias solo del MST
    N = set()                                     # Conjunto de nodos presentes en el MST
    for u, v, w in mst:
        g[u].append((v, w)); g[v].append((u, w))  # Inserta arista en ambos sentidos
        N.add(u); N.add(v)                        # Registra nodos
    parent = {n: (None, 0) for n in N}            # Padre de cada nodo y peso de la arista al padre
    children = {n: [] for n in N}                 # Hijos (a quién reenvía) por nodo
    if raiz in N:
        vis = {raiz}                              # Visitados para BFS sobre el MST
        q = deque([raiz])                         # Cola iniciada en la raíz
        while q:
            u = q.popleft()                       # Saca un nodo de la cola
            for v, w in g[u]:                     # Recorre sus vecinos en el MST
                if v not in vis:
                    vis.add(v)                    # Marca visitado
                    parent[v] = (u, w)            # Define padre de v y peso de esa arista
                    children[u].append((v, w))    # Agrega v como hijo (reenvío) de u
                    q.append(v)                   # Encola v para seguir el recorrido
    else:
        N.add(raiz)                               # Si el MST está vacío, agrega la raíz sola
        parent[raiz] = (None, 0)                  # La raíz no tiene padre
        children.setdefault(raiz, [])             # Asegura lista de hijos
    for k in children:
        children[k].sort(key=lambda x: x[0])      # Ordena hijos por nombre para salida estable
    return parent, children, N                     # Devuelve padres, hijos y conjunto de nodos del MST

def main():
    if not os.path.isfile(ALDEAS_FILE):           # Verifica que el archivo exista en la ruta esperada
        raise SystemExit(f"No se encontró el archivo de aldeas en: {ALDEAS_FILE}")

    edges = leer_aristas_csv_comas(ALDEAS_FILE)   # Lee todas las aristas del archivo
    if not edges:
        raise SystemExit("No se pudieron leer aristas del archivo.")  # Corta si no se obtuvo nada

    adj, nodos = grafo_no_dirigido(edges)         # Construye el grafo no dirigido mínimo por par

    if ORIGEN not in nodos:                       # Verifica que la aldea origen exista
        raise SystemExit(f"No existe la aldea origen '{ORIGEN}' en el archivo.")

    R = alcanzables(adj, ORIGEN)                  # Obtiene todas las aldeas alcanzables desde el origen
    if not R:
        raise SystemExit("No hay aldeas alcanzables desde el origen.")  # Caso límite

    mst, total = mst_kruskal(adj, R)              # Calcula el MST y su peso total

    esperadas = max(0, len(R) - 1)                # En un árbol con |R| nodos debe haber |R|-1 aristas
    if len(mst) != esperadas:
        raise SystemExit(f"El MST no es válido: {len(mst)} aristas, se esperaban {esperadas} para {len(R)} nodos.")

    parent, children, N = enraizar_mst(mst, ORIGEN)  # Enraiza el MST en la aldea origen
    if ORIGEN not in parent:                      # Garantiza que el origen aparezca en la salida
        parent[ORIGEN] = (None, 0)                # Origen sin padre
        children.setdefault(ORIGEN, [])           # Origen con lista de hijos
        N.add(ORIGEN)                              # Agrega origen al conjunto de nodos

    print("1) Aldeas alcanzables (alfabético):")  # Encabezado del listado 1
    for n in sorted(N):                           # Recorre las aldeas del árbol en orden alfabético
        print(f" - {n}")                          # Imprime cada aldea

    print(f"\n2) Plan de distribución (enraizado en '{ORIGEN}'):")  # Encabezado del listado 2
    for n in sorted(N):                           # Recorre aldeas en orden alfabético
        p, w = parent.get(n, (None, 0))           # Obtiene el padre y el peso de arista hacia el padre
        recibe = "(origen)" if p is None else f"{p} (dist={w})"  # Prepara el texto de “recibe de”
        env = ", ".join(f"{h} (dist={dw})" for h, dw in children.get(n, [])) or "(sin reenvíos)"  # “envía a”
        print(f" - {n}: recibe de {recibe}; envía a: {env}")      # Imprime la línea para la aldea

    print(f"\n3) Suma total de distancias (peso MST): {total}")   # Imprime el peso total del MST

if __name__ == "__main__":                          # Punto de entrada si se ejecuta como script
    main()                                          # Llama a la función principal