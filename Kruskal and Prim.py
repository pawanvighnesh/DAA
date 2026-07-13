import heapq
from typing import Dict, List, Tuple

Edge = Tuple[int, int, int]
AdjacencyList = Dict[int, List[Tuple[int, int]]]


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], int]:
    """Compute MST using Kruskal's algorithm.

    Args:
        n: Number of vertices.
        edges: List of edges as (weight, u, v).

    Returns:
        A tuple containing the MST edge list and total cost.
    """
    sorted_edges = sorted(edges)
    uf = UnionFind(n)
    mst: List[Tuple[int, int, int]] = []
    cost = 0

    for w, u, v in sorted_edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break

    if len(mst) != n - 1:
        raise ValueError("Graph is disconnected; MST does not exist.")

    return mst, cost


def prim(n: int, adj: AdjacencyList, start: int = 0) -> Tuple[List[Tuple[int, int, int]], int]:
    """Compute MST using Prim's algorithm.

    Args:
        n: Number of vertices.
        adj: Adjacency list mapping u -> [(v, weight), ...].
        start: Starting vertex.

    Returns:
        A tuple containing the MST edge list and total cost.
    """
    INF = float("inf")
    key = [INF] * n
    parent = [-1] * n
    in_mst = [False] * n
    key[start] = 0
    pq: List[Tuple[int, int]] = [(0, start)]
    mst: List[Tuple[int, int, int]] = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue

        in_mst[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):
            if not in_mst[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    if len(mst) != n - 1:
        raise ValueError("Graph is disconnected; MST does not exist.")

    return mst, cost


def build_adjacency_list(edges: List[Tuple[int, int, int]]) -> AdjacencyList:
    """Build adjacency list from an undirected weighted edge list."""
    adj: AdjacencyList = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


if __name__ == "__main__":
    n = 7
    edges = [
        (7, 0, 1),
        (5, 0, 3),
        (8, 1, 2),
        (9, 1, 3),
        (7, 1, 4),
        (5, 2, 4),
        (15, 3, 4),
        (6, 3, 5),
        (8, 4, 5),
        (9, 4, 6),
        (11, 5, 6),
    ]

    adj = build_adjacency_list(edges)

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj)

    print("=== Kruskal's MST ===")
    for u, v, w in k_mst:
        print(f" Edge ({u} - {v}) Weight: {w}")
    print(f" Total MST Cost: {k_cost}\n")

    print("=== Prim's MST ===")
    for u, v, w in p_mst:
        print(f" Edge ({u} - {v}) Weight: {w}")
    print(f" Total MST Cost: {p_cost}")
