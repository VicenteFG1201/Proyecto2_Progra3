from model.vertex import Vertex
from model.edge import Edge
import heapq

class Graph:
    def __init__(self):
        self.vertices = {}  # id -> Vertex
        self.edges = []

    def add_vertex(self, vertex):
        self.vertices[vertex.id] = vertex

    def add_edge(self, edge):
        self.edges.append(edge)
        edge.source.add_edge(edge)
        reverse = Edge(edge.destination, edge.source, edge.weight)
        edge.destination.add_edge(reverse)

    def calculate_route(self, origin_id, dest_id, algorithm="dijkstra"):
        if algorithm == "dijkstra":
            return self._dijkstra(origin_id, dest_id)
        # En el futuro se puede agregar Floyd-Warshall u otros aquí
        return []

    def _dijkstra(self, start_id, end_id):
        visited = set()
        min_heap = [(0, start_id, [])]

        while min_heap:
            cost, current_id, path = heapq.heappop(min_heap)
            if current_id in visited:
                continue
            visited.add(current_id)
            path = path + [current_id]
            if current_id == end_id:
                return path
            vertex = self.vertices[current_id]
            for edge in vertex.edges:
                if edge.destination.id not in visited:
                    heapq.heappush(min_heap, (cost + edge.weight, edge.destination.id, path))
        return None
