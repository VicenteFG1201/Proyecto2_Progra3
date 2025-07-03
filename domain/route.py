class Route:
    def __init__(self, path, cost):
        self.path = path  # lista de nodos
        self.cost = cost  # peso total o batería

    def __repr__(self):
        return f"Ruta: {' -> '.join(self.path)} | Costo: {self.cost}"
