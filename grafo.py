from typing import List, Dict, Optional, Tuple
from collections import defaultdict, deque
import time, random, copy

class Graph:
    def __init__(self):
        self.num_vertices = 0
        self.edge_count = 0
        self.adj_list: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        self.adj_matrix: Optional[List[List[Optional[float]]]] = None
        self.degrees: Dict[int, int] = defaultdict(int)
        
    def load_from_file(self, filepath: str):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            self.num_vertices = int(lines[0].strip())
            self.adj_matrix = [[None] * self.num_vertices for _ in range(self.num_vertices)]
            for line in lines[1:]:
                parts = line.strip().split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    weight = float(parts[2]) if len(parts) == 3 else 1.0
                    self.add_edge(u, v, weight)
            
    def get_neighbors(self, v: int) -> List[int]:
        return [i + 1 for i, weight in enumerate(self.adj_matrix[v - 1]) if weight is not None]
    
    def add_edge(self, u: int, v: int, weight: float = 1.0):
        self.adj_matrix[u - 1][v - 1] = weight
        self.edge_count += 1
        self.degrees[u] += 1
        
    def topological_sort_dfs(self) -> List[int]:
        visited = set()
        order = []
        on_stack = set()
        has_cycle = [False] 

        def dfs(v: int):
            visited.add(v)
            on_stack.add(v)
            for neighbor in self.get_neighbors(v):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in on_stack:
                    has_cycle[0] = True 
            on_stack.remove(v)
            order.append(v)

        for vertex in range(1, self.num_vertices + 1):
            if vertex not in visited:
                dfs(vertex)

        if has_cycle[0]:
            raise ValueError("O grafo tem ciclos!")

        return order[::-1]

    def topological_sort_kahn(self) -> List[int]:
        in_degree = {v: 0 for v in range(1, self.num_vertices + 1)}
        for v in range(1, self.num_vertices + 1):
            for neighbor in self.get_neighbors(v):
                in_degree[neighbor] += 1

        queue = deque([v for v in range(1, self.num_vertices + 1) if in_degree[v] == 0])
        order = []

        while queue:
            v = queue.popleft()
            order.append(v)
            for neighbor in self.get_neighbors(v):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != self.num_vertices:
            raise ValueError("O grafo tem ciclos!")

        return order

    def topological_sort_liu(self, in_degree: Dict[int, int], queue: deque) -> List[int]:
        order = []
        
        # Processa os vértices enquanto a fila não estiver vazia
        while queue:
            u = queue.popleft()
            order.append(u)

            # Processa os vizinhos de u
            for v in range(self.num_vertices):
                if self.adj_matrix[u - 1][v] is not None:  # Ajuste de índice para 0-based
                    in_degree[v + 1] -= 1  # Decrementa o grau de entrada de v (1-based)
                    if in_degree[v + 1] == 0:
                        queue.append(v + 1)  # Coloca v na fila se o grau de entrada for 0
        return order


# Função de pré-processamento que calcula os graus de entrada e a fila para Liu
def preparar_dados_para_ordem_topologica(grafo: Graph):
    # Calculando os graus de entrada para todos os algoritmos
    in_degree = {v: 0 for v in range(1, grafo.num_vertices + 1)}
    for v in range(1, grafo.num_vertices + 1):
        for neighbor in grafo.get_neighbors(v):
            in_degree[neighbor] += 1

    # Preparando fila de entrada 0 para o Liu
    queue = deque([v for v in range(1, grafo.num_vertices + 1) if in_degree[v] == 0])

    return in_degree, queue

# Função para testar os três algoritmos
def testar_algoritmos(grafo_base: Graph):
    resultados = {}

    # Pré-processamento dos dados (graus de entrada e fila)
    in_degree, queue = preparar_dados_para_ordem_topologica(grafo_base)

    # Kahn
    g_kahn = copy.deepcopy(grafo_base)  # Faz uma cópia profunda do grafo
    t0 = time.perf_counter()
    ordem_kahn = g_kahn.topological_sort_kahn()
    t1 = time.perf_counter()
    resultados['Kahn'] = (ordem_kahn, t1 - t0)

    # DFS
    g_dfs = copy.deepcopy(grafo_base)
    t0 = time.perf_counter()
    ordem_dfs = g_dfs.topological_sort_dfs()
    t1 = time.perf_counter()
    resultados['DFS'] = (ordem_dfs, t1 - t0)

    # Liu
    g_liu = copy.deepcopy(grafo_base)
    t0 = time.perf_counter()
    ordem_liu = g_liu.topological_sort_liu(in_degree, queue)  # Passando os dados pré-processados
    t1 = time.perf_counter()
    resultados['Liu'] = (ordem_liu, t1 - t0)

    return resultados
