from typing import List, Dict, Tuple
from collections import defaultdict, deque
import time, random, copy
class Graph:
    def __init__(self):
        self.num_vertices = 0
        self.edge_count = 0
        self.adj_list: Dict[int, List[int]] = defaultdict(list)
        self.edges: List[Tuple[int, int]] = []

    def load_from_file(self, filepath: str):
        with open(filepath, 'r') as file:
            lines = file.readlines()
            self.num_vertices = int(lines[0].strip())
            for line in lines[1:]:
                parts = line.strip().split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    self.add_edge(u, v)

    def add_edge(self, u: int, v: int):
        self.adj_list[u].append(v)
        self.edges.append((u, v))
        self.edge_count += 1

    def get_neighbors(self, v: int) -> List[int]:
        return self.adj_list[v]

    def topological_sort_kahn(self) -> List[int]:
        in_degree = {v: 0 for v in range(1, self.num_vertices + 1)}
        for u, v in self.edges:
            in_degree[v] += 1

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


    def topological_sort_liu(self) -> List[int]:
        # Cria lista de vértices
        order = list(range(1, self.num_vertices + 1))
        changed = True

        while changed:
            changed = False
            for u, v in self.edges:
                pos_u = order.index(u)
                pos_v = order.index(v)
                if pos_u > pos_v:
                    order[pos_u], order[pos_v] = order[pos_v], order[pos_u]
                    changed = True

        return order

# Função para gerar entrada aleatória de um DAG
def gerar_entrada_aleatoria(nome_arquivo, num_vertices=None, num_arestas=None):
    if num_vertices is None:
        num_vertices = random.randint(10, 100)  # 10 a 100 vértices
    if num_arestas is None:
        num_arestas = random.randint(num_vertices - 1, num_vertices * (num_vertices - 1) // 2)

    with open(nome_arquivo, 'w') as f:
        f.write(f"{num_vertices}\n")
        
        arestas = set()
        while len(arestas) < num_arestas:
            v1 = random.randint(1, num_vertices)
            v2 = random.randint(1, num_vertices)
            if v1 < v2:
                arestas.add((v1, v2))


        for v1, v2 in arestas:
            f.write(f"{v1} {v2} 1\n")


def testar_algoritmos(grafo_base: Graph, repeticoes: int = 100):
    resultados = {'Kahn': [], 'DFS': [], 'Liu': []}
    execucoes_exemplo = {}

    for _ in range(repeticoes):
        for nome, metodo in {
            'Kahn': Graph.topological_sort_kahn,
            'DFS': Graph.topological_sort_dfs,
            'Liu': Graph.topological_sort_liu
        }.items():
            g_copia = copy.deepcopy(grafo_base)
            t0 = time.perf_counter()
            resultado = metodo(g_copia)
            t1 = time.perf_counter()
            resultados[nome].append(t1 - t0)

            if nome not in execucoes_exemplo:
                execucoes_exemplo[nome] = resultado


    medias = {
        alg: (execucoes_exemplo[alg], sum(tempos) / len(tempos))
        for alg, tempos in resultados.items()
    }

    return medias
