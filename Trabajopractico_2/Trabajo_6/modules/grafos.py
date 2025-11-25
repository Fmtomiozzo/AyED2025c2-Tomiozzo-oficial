from typing import Dict, List, Tuple, Set
from modules.cola_prioridad import ColaPrioridad


class Grafo:
    """
    Grafo NO dirigido, ponderado, representado con lista de adyacencia.
    adj[u] = lista de (v, peso).
    """

    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {}
        self.nodos: Set[str] = set()

    def agregar_nodo(self, u: str):
        if u not in self.adj:
            self.adj[u] = []
            self.nodos.add(u)

    def agregar_arista(self, u: str, v: str, w: int):
        """
        Agrega una arista no dirigida u --w-- v.
        Si ya existe entre el par (u,v), se queda con el menor peso.
        """
        self.agregar_nodo(u)
        self.agregar_nodo(v)

        # Actualizar/insertar u -> v
        reemplazar = True
        for i, (vx, wx) in enumerate(self.adj[u]):
            if vx == v:
                if w < wx:
                    self.adj[u][i] = (v, w)
                reemplazar = False
                break
        if reemplazar:
            self.adj[u].append((v, w))

        # Actualizar/insertar v -> u
        reemplazar = True
        for i, (ux, wx) in enumerate(self.adj[v]):
            if ux == u:
                if w < wx:
                    self.adj[v][i] = (u, w)
                reemplazar = False
                break
        if reemplazar:
            self.adj[v].append((u, w))

    def vecinos(self, u: str) -> List[Tuple[str, int]]:
        return self.adj.get(u, [])

    def contiene(self, u: str) -> bool:
        return u in self.adj


def construir_grafo_no_dirigido(edges: List[Tuple[str, str, int]]) -> Grafo:
    """
    A partir de una lista de aristas (u, v, w), construye un grafo no dirigido.
    Si hay múltiples aristas entre el mismo par, queda la de menor peso.
    """
    g = Grafo()
    for u, v, w in edges:
        g.agregar_arista(u, v, w)
    return g


def alcanzables(g: Grafo, s: str) -> Set[str]:
    """
    BFS para obtener todos los nodos alcanzables desde s.
    Implementado con una lista como cola (sin deque).
    """
    if not g.contiene(s):
        return set()

    visitado = {s}
    q: List[str] = [s]

    while q:
        u = q.pop(0)
        for v, _ in g.vecinos(u):
            if v not in visitado:
                visitado.add(v)
                q.append(v)

    return visitado


def mst_prim(g: Grafo, raiz: str):
    """
    Algoritmo de Prim para obtener el Árbol de Expansión Mínima (MST)
    partiendo de 'raiz'.

    Devuelve (mst, total):
      - mst: lista de aristas (u, v, w)
      - total: suma de los pesos
    """
    if not g.contiene(raiz):
        return [], 0

    visitado: Set[str] = {raiz}
    pq = ColaPrioridad()

    # Inicializar cola de prioridad con aristas que salen de la raíz
    for v, w in g.vecinos(raiz):
        # prioridad = peso
        pq.insertar(w, (raiz, v, w))

    mst: List[Tuple[str, str, int]] = []
    total = 0

    while not pq.esta_vacia():
        u, v, w = pq.extraer()  # dato = (u, v, w)
        if v in visitado:
            continue

        # Agregamos arista al MST
        visitado.add(v)
        mst.append((u, v, w))
        total += w

        # Agregamos las aristas que salen de v
        for x, wx in g.vecinos(v):
            if x not in visitado:
                pq.insertar(wx, (v, x, wx))

    return mst, total


def enraizar_mst(mst: List[Tuple[str, str, int]], raiz: str):
    """
    A partir de la lista de aristas del MST, construye:

    - parent: dict nodo -> (padre, peso_a_padre)
    - children: dict nodo -> lista[(hijo, peso)]
    - N: conjunto de nodos del MST
    """
    g_temp: Dict[str, List[Tuple[str, int]]] = {}
    N: Set[str] = set()

    def agregar_nodo_local(u: str):
        if u not in g_temp:
            g_temp[u] = []

    for u, v, w in mst:
        agregar_nodo_local(u)
        agregar_nodo_local(v)
        g_temp[u].append((v, w))
        g_temp[v].append((u, w))
        N.add(u)
        N.add(v)

    parent: Dict[str, Tuple[str, int]] = {n: (None, 0) for n in N}
    children: Dict[str, List[Tuple[str, int]]] = {n: [] for n in N}

    if raiz in N:
        vis: Set[str] = {raiz}
        q: List[str] = [raiz]

        while q:
            u = q.pop(0)
            for v, w in g_temp.get(u, []):
                if v not in vis:
                    vis.add(v)
                    parent[v] = (u, w)
                    children[u].append((v, w))
                    q.append(v)
    else:
        # Caso borde: MST vacío o raíz no incluida
        N.add(raiz)
        parent[raiz] = (None, 0)
        children.setdefault(raiz, [])

    # Ordenar los hijos alfabéticamente por nombre de nodo (opcional)
    for k in children:
        children[k].sort(key=lambda x: x[0])

    return parent, children, N