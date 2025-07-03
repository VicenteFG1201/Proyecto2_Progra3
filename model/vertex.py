class Vertex:
    def __init__(self, id):
        self.id = id
        self.role = None  # 'storage', 'recharge', 'client'
        self.edges = []

    def __repr__(self):
        return f"Vertex({self.id}, role={self.role})"

    def add_edge(self, edge):
        self.edges.append(edge)
