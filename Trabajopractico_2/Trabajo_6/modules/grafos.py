from collections import defaultdict, deque
import heapq


def grafo_no_dirigido(edges):
    """
    Construye una lista de adyacencia mínima (por par de aldeas) a partir
    de las aristas (u, v, w). Si hay múltiples aristas entre el mismo par,
    se queda con el menor peso.
    """
    best = {}          # (u,v) ordenado -> mejor peso
    nodos = set()
    for u, v, w in edges:
        nodos.add(u)
        nodos.add(v)
        k = tuple(sorted((u, v)))
        if k not in best or w < best[k]:
            best[k] = w

    adj = defaultdict(list)
    for (u, v), w in best.items():
        adj[u].append((v, w))
        adj[v].append((u, w))

    return adj, nodos


def alcanzables(adj, s):
    """
    BFS para obtener todos los nodos alcanzables desde s.
    """
    vis = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if v not in vis:
                vis.add(v)
                q.append(v)
    return vis


def mst_prim(adj, raiz):
    """
    Algoritmo de Prim para obtener el Árbol de Expansión Mínima (MST)
    partiendo de 'raiz'. Devuelve (mst, total):

      - mst: lista de aristas (u, v, w)
      - total: suma de los pesos
    """
    if raiz not in adj:
        return [], 0

    visitado = set([raiz])
    heap = []

    # Inicializar heap con las aristas que salen de la raíz
    for v, w in adj[raiz]:
        heapq.heappush(heap, (w, raiz, v))

    mst = []
    total = 0

    while heap:
        w, u, v = heapq.heappop(heap)
        if v in visitado:
            continue
        # Agregamos arista al MST
        visitado.add(v)
        mst.append((u, v, w))
        total += w

        # Nuevas aristas que salen de v
        for x, wx in adj[v]:
            if x not in visitado:
                heapq.heappush(heap, (wx, v, x))

    return mst, total


def enraizar_mst(mst, raiz):
    """
    A partir de la lista de aristas del MST, construye:

      - parent: dict nodo -> (padre, peso_a_padre)
      - children: dict nodo -> lista[(hijo, peso)]
      - N: conjunto de nodos del MST
    """
    g = defaultdict(list)
    N = set()
    for u, v, w in mst:
        g[u].append((v, w))
        g[v].append((u, w))
        N.add(u)
        N.add(v)

    parent = {n: (None, 0) for n in N}
    children = {n: [] for n in N}

    if raiz in N:
        from collections import deque

        vis = {raiz}
        q = deque([raiz])
        while q:
            u = q.popleft()
            for v, w in g[u]:
                if v not in vis:
                    vis.add(v)
                    parent[v] = (u, w)
                    children[u].append((v, w))
                    q.append(v)
    else:
        # Caso borde: si el MST está vacío o no incluye la raíz
        N.add(raiz)
        parent[raiz] = (None, 0)
        children.setdefault(raiz, [])

    for k in children:
        children[k].sort(key=lambda x: x[0])

    return parent, children, N